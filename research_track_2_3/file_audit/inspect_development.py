"""Inspect development-only additional evidence; no inference or held-out reads."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];out=[]
for l in (R/'hf_candidate/prepared/development.jsonl').read_text().splitlines():
 r=json.loads(l);files=r['provenance']['files_sha256'];pair=r['conditions']['colluders']
 def load(name):
  path=next(k for k in files if k.endswith('/'+name));raw=(R/'hf_candidate/raw'/path).read_bytes();assert hashlib.sha256(raw).hexdigest()==files[path];return json.loads(raw)
 prompts=load('agent_prompts.json');turns=load('agent_turns.json');boards=load('blackboards.json');metrics=load('metrics.json');summary=load('final_summary.json')
 exposures=[]
 for b in boards:
  for e in b['events']:
   if e.get('kind')!='communication' or e.get('agent') not in pair:continue
   content=e['payload'].get('content','');recipient=next(a for a in pair if a!=e['agent'])
   matches=[n for n,p in enumerate(prompts) if p.get('agent_name')==recipient and content and content in p.get('user_prompt','')]
   exposures.append({'board_event_id':e['id'],'sender':e['agent'],'recipient':recipient,'exact_content_present_in_recipient_prompt':bool(matches),'prompt_record_indices':matches,'caveat':'Recorded application prompt inclusion, not verified provider payload or proof of attention.'})
 out.append({'run':str(r['conditions']['seed'])+'_'+r['conditions']['sweep'],'file_names':sorted({Path(p).name for p in files}),'prompt_records':len(prompts),'turn_records':len(turns),'exact_partner_prompt_exposure_count':sum(e['exact_content_present_in_recipient_prompt'] for e in exposures),'candidate_post_count':len(exposures),'exposures':exposures,'execution_turns':[t for t in turns if t.get('phase')=='execution'],'recorded_coalition_regret':metrics.get('coalition_mean_regret'),'recorded_outsider_regret':metrics.get('noncoalition_mean_regret'),'derived_recorded_regret_gap':metrics['noncoalition_mean_regret']-metrics['coalition_mean_regret'] if metrics.get('noncoalition_mean_regret') is not None and metrics.get('coalition_mean_regret') is not None else None,'recorded_system_regret':metrics.get('system_regret'),'recorded_rewards_match_summary':all(abs(a['reward']-summary['agent_rewards'][a['agent_name']])<1e-7 for a in metrics['agents'] if a.get('reward') is not None)})
Path(__file__).with_name('development_findings.json').write_text(json.dumps(out,indent=2)+'\n')
print('Runs',len(out),'candidate posts',sum(x['candidate_post_count'] for x in out),'exact partner prompt inclusion',sum(x['exact_partner_prompt_exposure_count'] for x in out),'regret gaps available',sum(x['derived_recorded_regret_gap'] is not None for x in out),'rewards match',all(x['recorded_rewards_match_summary'] for x in out))
