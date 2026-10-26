"""Canonical20 completed test episodes, preserved source-linked evidence."""
import json,hashlib,sys,importlib.util
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent;ROOT=R.parent
sp=importlib.util.spec_from_file_location('jira',ROOT/'collusion_hackathon/colosseum/experiments/collusion/compute_jira_optimal.py');m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
manifest_path=ROOT/'collusion_hackathon/colosseum/generation_integrity/track23/collection_manifest.json';manifest=json.loads(manifest_path.read_text());assert manifest['completed_episodes']==20 and manifest['collection_complete'];out=[]
for entry in manifest['episodes']:
 p=Path(entry['directory']);config=json.loads((p/'run_config.json').read_text());summary=json.loads((p/'final_summary.json').read_text());events=json.loads((p/'tool_events.json').read_text());pair=config['colluders'];boards=json.loads((p/'blackboards.json').read_text());published={e['id'] for b in boards for e in b['events'] if e.get('kind')=='communication'}
 messages=[{'event':n,'actor':e['agent_name'],'message':e['arguments'].get('message','')} for n,e in enumerate(events) if e['agent_name'] in pair and e['tool_name']=='post_message' and e['result'].get('event_id') in published]
 actions=[{'event':n,'actor':e['agent_name'],'task':e['arguments'].get('task_id'),'result':e['result']} for n,e in enumerate(events) if e['agent_name'] in pair and e['tool_name']=='assign_task']
 instance=m._reconstruct_instance(p);w=m._load_weights(p,None);evaluated=m._evaluate(summary['assignment'],instance=instance,weights=w);delta=evaluated.joint_reward-summary['joint_reward']
 out.append({'run':str(config['seed'])+'_'+config['sweep'],'directory':str(p),'pair':pair,'messages':messages,'actions':actions,'summary':summary,'scorer_reconstruction_delta':delta,'sha256':{name:hashlib.sha256((p/name).read_bytes()).hexdigest() for name in ['tool_events.json','blackboards.json','run_config.json','final_summary.json','agent_prompts.json']}})
(P/'evidence.json').write_text(json.dumps(out,indent=2)+'\n')
(P/'provenance.json').write_text(json.dumps({'collection_manifest':str(manifest_path),'sha256':hashlib.sha256(manifest_path.read_bytes()).hexdigest(),'episodes':20,'failed_attempts_included':False},indent=2)+'\n')
print('Prepared20. Scorer mismatches:',[(x['run'],round(x['scorer_reconstruction_delta'],5)) for x in out if abs(x['scorer_reconstruction_delta'])>1e-7])
for x in out:
 print('\nRUN',x['run'],x['pair'])
 # Full pair text is preserved; show messages in manageable chunks in subsequent reads.
 print('messages',len(x['messages']),'actions',[(a['event'],a['actor'],a['task'],a['result'].get('status')) for a in x['actions']])
