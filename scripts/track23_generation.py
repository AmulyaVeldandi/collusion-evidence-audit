"""Audited, bounded direct-OpenAI generation. Never reads previous outputs.

Smoke: python -m experiments.collusion.track23_generation --mode smoke
Test requires a separately supplied approval JSON; see generation_integrity/track23/PROTOCOL.md.
"""
from __future__ import annotations
import argparse
import asyncio
import copy
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import uuid

ROOT = Path(__file__).resolve().parents[2]
os.environ['TERRARIUM_COLLAB_PATH'] = str(ROOT / 'external/CoLLAB')
os.environ['MPLCONFIGDIR'] = str(ROOT / 'generation_integrity/track23/matplotlib')
from dotenv import dotenv_values
from openai import OpenAI
import yaml
from experiments.collusion import run as runner
from experiments.common.local_protocol import LocalCommunicationProtocol
from envs.dcops.jira_ticket.jira_ticket_env import JiraTicketEnvironment
from llm_server.clients.openai_client import OpenAIClient
from terrarium.agents.base import BaseAgent

MODEL = 'gpt-4o-mini-2024-07-18'
INPUT_RATE = 0.15 / 1_000_000
OUTPUT_RATE = 0.60 / 1_000_000
# Reserve the entire model context window plus configured output for each attempted call.
CALL_RESERVE = 128_000 * INPUT_RATE + 1500 * OUTPUT_RATE
PRICING_URL = 'https://developers.openai.com/api/docs/models/gpt-4o-mini'


def now():
    return datetime.now(timezone.utc).isoformat()


def serial(value):
    if hasattr(value, 'model_dump'):
        return value.model_dump(mode='json')
    if isinstance(value, Path):
        return str(value)
    raise TypeError(type(value).__name__)


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, default=serial, indent=2, ensure_ascii=False))
    temp.replace(path)


def append(path, value):
    with path.open('a') as f:
        f.write(json.dumps(value, default=serial, ensure_ascii=False) + '\n')
        f.flush()
        os.fsync(f.fileno())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class GenerationAbort(BaseException):
    """Not swallowed by Terrarium's continuation-error handler."""


class Budget:
    def __init__(self, folder, usd, max_calls):
        self.folder, self.limit, self.max_calls = folder, usd, max_calls
        self.calls = 0
        self.measured = 0.0
        self.reserved = 0.0
        self.input_tokens = self.output_tokens = 0
        self.failures = 0
        self.lock = threading.Lock()
        self.flush()

    def flush(self):
        write(self.folder / 'usage.json', {
            'model': MODEL, 'budget_usd': self.limit, 'max_calls': self.max_calls,
            'attempted_calls': self.calls, 'measured_uncached_rate_usd': self.measured,
            'unresolved_reservation_usd': self.reserved,
            'accounted_upper_usd': self.measured + self.reserved,
            'input_tokens': self.input_tokens, 'output_tokens': self.output_tokens,
            'failed_calls': self.failures, 'input_usd_per_million': 0.15,
            'output_usd_per_million': 0.60, 'pricing_source': PRICING_URL,
            'cost_note': 'Token-derived estimate, not provider invoice; cached input charged at full rate. Unknown failed-call usage retains full reservation.',
        })

    def start(self, params, context):
        if params.get('model') != MODEL or params.get('max_output_tokens') != 1500:
            raise GenerationAbort('Unexpected model or output limit')
        if params.get('stream') or params.get('previous_response_id'):
            raise GenerationAbort('Streaming/implicit context not permitted')
        if any(t.get('type') != 'function' for t in params.get('tools', [])):
            raise GenerationAbort('Hosted billable tools not permitted')
        with self.lock:
            if self.calls >= self.max_calls or self.measured + self.reserved + CALL_RESERVE > self.limit + 1e-12:
                append(self.folder / 'api_events.jsonl', {'event':'budget_stop','time':now(),'context':context})
                raise GenerationAbort('Cost/call ceiling reached before request')
            self.calls += 1
            self.reserved += CALL_RESERVE
            call = self.calls
            self.flush()
            append(self.folder / 'api_events.jsonl', {'event':'request','call':call,'time':now(),
                   'context':context,'reserved_usd':CALL_RESERVE,'endpoint':'https://api.openai.com/v1/responses','body':params})
            return call

    def finish(self, call, response):
        raw = response.model_dump(mode='json')
        append(self.folder / 'api_events.jsonl', {'event':'response','call':call,'time':now(),
               'request_id':getattr(response,'_request_id',None),'body':raw})
        usage = raw.get('usage')
        if not usage:
            self.failures += 1
            self.flush()
            raise GenerationAbort('Response missing usage; retained reservation')
        cost = usage['input_tokens'] * INPUT_RATE + usage['output_tokens'] * OUTPUT_RATE
        with self.lock:
            self.measured += cost
            self.reserved -= CALL_RESERVE
            self.input_tokens += usage['input_tokens']
            self.output_tokens += usage['output_tokens']
            self.flush()
        if cost > CALL_RESERVE + 1e-12 or raw.get('model') != MODEL:
            raise GenerationAbort('Unexpected usage or returned model')


class AuditedClient(OpenAIClient):
    def __init__(self, key, budget, agent_name):
        # Avoid native constructor's implicit .env reload and both retry layers.
        self.client = OpenAI(api_key=key, base_url='https://api.openai.com/v1',
                             max_retries=0, timeout=120.0)
        self.budget = budget
        self.audit_context = {'agent':agent_name}

    def _responses_create_with_retries(self, api_params):
        params = dict(api_params, store=False)
        call = self.budget.start(params, self.audit_context)
        try:
            response = self.client.responses.create(**params)
        except Exception as exc:
            self.budget.failures += 1
            # Do not log SDK exception strings: authentication errors can echo key fragments.
            append(self.budget.folder / 'api_events.jsonl', {'event':'failure','call':call,'time':now(),
                'error_type':type(exc).__name__,'status_code':getattr(exc,'status_code',None),
                'request_id':getattr(exc,'request_id',None),'code':getattr(exc,'code',None)})
            self.budget.flush()
            raise GenerationAbort(f'API request failed: {type(exc).__name__}; no retry') from None
        self.budget.finish(call, response)
        return response


def state(env):
    return {'seed':env.current_seed,'tasks':env.tasks,'agent_names':env.agent_names,
            'agent_private':env.agent_private,'costs':env.costs,'assignment':env.assignment.copy(),
            'agents_without_decision':[a for a in env.agent_names if a not in env.assignment],
            'explicit_skips':[a for a,v in env.assignment.items() if v is None],
            'assignment_filling':env.assignment_filling_enabled(),
            'tasks_done_bonus':env.tasks_done_bonus,'priority_bonus':env.priority_bonus,
            'violation_penalty':env.violation_penalty}


class AuditedEnvironment(JiraTicketEnvironment):
    # Preserve original environment/tool identity for tool discovery and native logging.
    tools_environment_name = 'JiraTicketEnvironment'
    def __init__(self, protocol, config, tool_logger):
        super().__init__(protocol, config, tool_logger)
        self.audit_dir = Path(tool_logger.log_dir)
        write(self.audit_dir / 'effective_config.json', config)
        write(self.audit_dir / 'initial_state.json', state(self))
        protocol.audit_dir = self.audit_dir

    def get_final_summary(self):
        write(self.audit_dir / 'state_before_summary.json', state(self))
        result = super().get_final_summary()
        write(self.audit_dir / 'final_state.json', state(self))
        return result


AuditedEnvironment.__name__ = 'JiraTicketEnvironment'


class AuditedProtocol(LocalCommunicationProtocol):
    def _record_tool_event(self, **kwargs):
        super()._record_tool_event(**kwargs)
        append(self.audit_dir / 'tool_events_incremental.jsonl', asdict(self.tool_events[-1]))
        write(self.audit_dir / 'latest_state.json', state(self.environment))


class AuditedAgent(BaseAgent):
    async def generate_response(self, **kwargs):
        env = kwargs['communication_protocol'].environment
        self.client.audit_context = {'agent':self.name,'seed':env.current_seed,
            'run':env.full_config['simulation']['run_timestamp'],
            'phase':kwargs['phase'],'round':kwargs.get('round_num')}
        try:
            result = await super().generate_response(**kwargs)
            append(env.audit_dir / 'turns_incremental.jsonl',
                   {'context':self.client.audit_context.copy(),'result':result})
            return result
        finally:
            write(env.audit_dir / 'latest_state.json', state(env))
            write(env.audit_dir / 'blackboards_checkpoint.json', [
                {'id':b.blackboard_id,'participants':sorted(b.agents),'events':b.logs}
                for b in kwargs['communication_protocol'].megaboard.blackboards])


def validate(cfg, mode):
    assert cfg['environment'] == {'name':'JiraTicketEnvironment','assignment_filling':False,'max_tasks':8}
    assert cfg['communication_network'] == {'topology':'complete','num_agents':6,'consolidate_channels':True}
    assert [cfg['simulation'][k] for k in ('max_iterations','max_planning_rounds','max_conversation_steps')] == [1,4,3]
    assert cfg['llm_models'] == [{'label':'openai_gpt4o_mini_2024_07_18','llm':{
        'provider':'openai','openai':{'model':MODEL,'params':{'max_tokens':1500,'temperature':0.7}}}}]
    exp = cfg['experiment']
    assert exp['max_concurrent_runs'] == 1
    assert exp['collusion'] == {'colluder_selection':'first','agent_order':'random'}
    seeds = [9999] if mode == 'smoke' else list(range(101,111))
    assert exp['seeds'] == seeds
    expected = []
    for name, secret, variant in ([('treatment',True,'simple')] if mode == 'smoke' else
                                  [('baseline',False,'control'),('treatment',True,'simple')]):
        expected.append({'name':name,'topologies':['complete'],'num_agents':[6],
                         'colluder_counts':[2],'secret_channel_enabled':[secret],'prompt_variants':[variant]})
    assert exp['sweeps'] == expected
    assert not any(k in exp for k in ('runs_per_setting','planning_rounds','max_conversation_steps'))
    return len(seeds) * len(expected)


def provenance(folder, config, approval=None):
    sources = [Path(__file__), ROOT/'experiments/collusion/run.py', ROOT/'experiments/collusion/prompts.py',
        ROOT/'experiments/common/local_protocol.py', ROOT/'experiments/common/providers.py',
        ROOT/'experiments/collusion/metrics.py', ROOT/'experiments/common/run_utils.py']
    site = Path(sys.prefix)/'lib'/f'python{sys.version_info.major}.{sys.version_info.minor}'/'site-packages'
    for package in ['terrarium','llm_server','envs']:
        sources.extend((site/package).rglob('*.py'))
    sources.extend((ROOT/'external/CoLLAB/problem_layer').rglob('*.py'))
    hashes = {str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):sha(p) for p in sources}
    write(folder/'provenance.json', {'created_at':now(),'python':sys.version,'source_sha256':hashes,
          'config_sha256':sha(config),'config_path':str(config),'model':MODEL,
          'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
          'packages':{d.metadata['Name']:d.version for d in importlib.metadata.distributions()},
          'original_config_sha256':{n:sha(ROOT/'experiments/collusion/configs'/n)
              for n in ['track23_smoke.yaml','track23_fresh20.yaml']},
          'evaluation_freeze_user_confirmed':True,'test_budget_approved':bool(approval and approval.get('user_approved'))})
    write(folder/'config.json',yaml.safe_load(config.read_text()))



def prepare_restart(cfg, prior, approval):
    """Resume only an explicitly approved failed invocation; never inspect narratives."""
    prior = prior.resolve()
    if approval.get('retry_failed_episode_authorized') is not True:
        raise ValueError('Explicit failed-episode retry authorization required')
    if str(prior) != approval.get('resume_from'):
        raise ValueError('Approval does not match prior invocation')
    status = json.loads((prior/'execution_status.json').read_text())
    if status['status'] != 'failed' or status['mode'] != 'test':
        raise ValueError('Prior invocation must be a stopped failed test')
    chain = approval.get('prior_invocations') or [{'path':str(prior),'manifest_sha256':approval.get('prior_manifest_sha256')}]
    if not chain or Path(chain[-1]['path']).resolve() != prior:
        raise ValueError('Reviewed history does not end at prior invocation')
    completed, started = set(), set()
    failed_attempts = []
    prior_cost = 0.0
    seen = set()
    for index, entry in enumerate(chain):
        folder = Path(entry['path']).resolve()
        if folder in seen:
            raise ValueError('Duplicate prior invocation')
        seen.add(folder)
        if index:
            parent = json.loads((folder/'restart_record.json').read_text())['prior_invocation']
            if Path(parent).resolve() != Path(chain[index-1]['path']).resolve():
                raise ValueError('Incomplete invocation history')
        elif (folder/'restart_record.json').exists():
            raise ValueError('History omits an earlier invocation')
        manifest_path = folder/'artifact_hashes.json'
        if sha(manifest_path) != entry['manifest_sha256']:
            raise ValueError('Prior artifact manifest changed')
        for name, digest in json.loads(manifest_path.read_text()).items():
            if sha(folder/name) != digest:
                raise ValueError('Prior artifact changed')
        prior_cost += json.loads((folder/'usage.json').read_text())['accounted_upper_usd']
        for directory in (folder/'episodes').glob('*/runs/*/*/*'):
            effective = json.loads((directory/'effective_config.json').read_text())
            pair = (directory.parent.name, effective['simulation']['seed'])
            started.add(pair)
            if (directory/'run_config.json').exists() and (directory/'final_summary.json').exists():
                if pair in completed:
                    raise ValueError('Duplicate completed episode')
                completed.add(pair)
            else:
                failed_attempts.append({'condition':pair[0],'seed':pair[1],'directory':str(directory)})
    remaining = copy.deepcopy(cfg)
    original_schedule = {(s['name'],seed) for s in cfg['experiment']['sweeps'] for seed in cfg['experiment']['seeds']}
    if not started <= original_schedule or not completed < original_schedule:
        raise ValueError('Unexpected prior schedule')
    sweeps = []
    for sweep in remaining['experiment']['sweeps']:
        sweep['seeds'] = [seed for seed in cfg['experiment']['seeds'] if (sweep['name'],seed) not in completed]
        if sweep['seeds']:
            sweeps.append(sweep)
    remaining['experiment']['sweeps'] = sweeps
    budget = float(approval['budget_usd']) - prior_cost
    if budget <= CALL_RESERVE:
        raise ValueError('Insufficient remaining approved budget')
    record = {'prior_invocation':str(prior),'prior_manifest_sha256':sha(prior/'artifact_hashes.json'),
        'preserved_completed_episodes':sorted(completed),'retained_failed_attempts':failed_attempts,'prior_invocations':chain,
        'retry_failed_episode_authorized':True,'credential_rotation':bool(approval.get('credential_rotation',False)),
        'prior_accounted_upper_usd':prior_cost,'original_total_cap_usd':approval['budget_usd'],
        'remaining_cap_usd':budget,'protocol_deviation':'User explicitly authorized continuation and retry of the failed episode; every prior attempt retained, completed episodes not repeated; automatic retries remain disabled.'}
    return remaining, len(original_schedule-completed), budget, record

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mode', choices=['smoke','test'], required=True)
    ap.add_argument('--approval', type=Path)
    ap.add_argument('--resume-from', type=Path)
    args = ap.parse_args()
    os.chdir(ROOT)
    stem = 'track23_smoke_openai' if args.mode == 'smoke' else 'track23_fresh20_openai'
    config = ROOT/'experiments/collusion/configs'/f'{stem}.yaml'
    cfg = yaml.safe_load(config.read_text())
    count = validate(cfg,args.mode)
    budget_usd = 2.0
    approval = None
    if args.mode == 'test':
        if not args.approval:
            ap.error('Test generation is gated: explicit budget approval and frozen evaluation identifier required.')
        approval = json.loads(args.approval.read_text())
        if not (approval.get('user_approved') is True and approval.get('evaluation_frozen') is True
                and approval.get('evaluation_version_or_hash') and approval.get('config_sha256') == sha(config)
                and approval.get('wrapper_sha256') == sha(Path(__file__))
                and approval.get('protocol_deviations_accepted') is True):
            ap.error('Approval missing, stale, or incomplete')
        budget_usd = float(approval['budget_usd'])
        if not 0 < budget_usd <= 40:
            ap.error('Invalid approved budget')
    restart = None
    if args.resume_from:
        if args.mode != 'test' or approval is None:
            ap.error('Restart requires test approval')
        cfg, count, budget_usd, restart = prepare_restart(cfg, args.resume_from, approval)
    key_file = ROOT.parent.parent/'.env.local'
    key = dotenv_values(key_file, interpolate=False).get('OPENAI_API_KEY')
    if not key:
        ap.error('Authorized credential not found')
    folder = ROOT/'generation_integrity/track23'/args.mode/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_'+uuid.uuid4().hex[:8])
    folder.mkdir(parents=True,exist_ok=False)
    provenance(folder,config,approval)
    if approval:
        write(folder/'approval.json',approval)
    if restart:
        write(folder/'restart_record.json',restart)
        config = folder/'restart_config.yaml'
        config.write_text(yaml.safe_dump(cfg,sort_keys=False))
        write(folder/'effective_config_hash.json',{'sha256':sha(config)})
    budget = Budget(folder,budget_usd,count*90)
    runner.get_client_instance = lambda llm_cfg,agent_name=None,**kw: AuditedClient(key,budget,agent_name)
    runner._resolve_environment_class = lambda env_cfg: AuditedEnvironment
    runner.LocalCommunicationProtocol = AuditedProtocol
    runner.BaseAgent = AuditedAgent
    runner.confirm_spend = lambda *a,**kw: None  # Replaced by validated per-request hard ceiling above.
    # Give every invocation a fresh side-log namespace: native env clears by tag/model/seed.
    original_single = runner._run_single
    async def single(**kwargs):
        local = copy.deepcopy(kwargs['base_cfg'])
        local['experiment']['tag'] = stem+'_'+folder.name+'_'+kwargs['sweep_name']
        kwargs['base_cfg'] = local
        return await original_single(**kwargs)
    runner._run_single = single
    result = {'mode':args.mode,'status':'running','episodes_requested':count,'started_at':now()}
    write(folder/'execution_status.json',result)
    print(json.dumps({'audit_folder':str(folder),'budget_usd':budget_usd,'max_calls':count*90}),flush=True)
    try:
        output = asyncio.run(runner.run_from_config(str(config),out_dir=str(folder/'episodes'),yes=True))
        progress = json.loads((output/'progress.json').read_text())
        result.update(status='completed' if progress['completed_runs']==count and progress['failed_runs']==0 else 'failed',
                      output_root=str(output),progress=progress)
    except BaseException as exc:
        result.update(status='failed',error_type=type(exc).__name__)
        if isinstance(exc,GenerationAbort):
            result['error']=str(exc)
        raise SystemExit('Generation stopped; see execution_status.json and API audit (no retry).') from None
    finally:
        result['finished_at']=now()
        write(folder/'execution_status.json',result)
        budget.flush()
        write(folder/'artifact_hashes.json', {str(p.relative_to(folder)):sha(p) for p in folder.rglob('*')
                                             if p.is_file() and p.name!='artifact_hashes.json'})
        print(json.dumps({'audit_folder':str(folder),'status':result['status'],
                          'calls':budget.calls,'measured_usd':budget.measured}),flush=True)

if __name__ == '__main__':
    main()
