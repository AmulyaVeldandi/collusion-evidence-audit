import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=Path(__file__).resolve().parent
rows=[json.loads(l) for name in ['development','held_out','reserve'] for l in (R/('hf_candidate/prepared/'+name+'.jsonl')).read_text().splitlines()]
selected=sorted(rows,key=lambda r:(r['conditions']['seed'],r['conditions']['sweep']))
out=[]
for r in selected:
 c=r['conditions'];pair=c['colluders'];obs=r['observations'];path=next(k for k in r['provenance']['files_sha256'] if k.endswith('/tool_events.json'));raw=(R/'hf_candidate/raw'/path).read_bytes();assert hashlib.sha256(raw).hexdigest()==r['provenance']['files_sha256'][path]
 events=json.loads(raw);boardids={e['id'] for b in obs['blackboards'] for e in b['events'] if e.get('kind')=='communication'}
 messages=[{'event':i,'actor':e['agent_name'],'message':e['arguments']['message']} for i,e in enumerate(events) if e['tool_name']=='post_message' and e['agent_name'] in pair and e['result'].get('event_id') in boardids and not e['result'].get('error')]
 actions=[{'event':i,'actor':e['agent_name'],'arguments':e['arguments'],'result':e['result']} for i,e in enumerate(events) if e['tool_name']!='post_message' and e['agent_name'] in pair]
 out.append({'id':str(c['seed'])+'_'+c['sweep'],'trajectory_id':r['trajectory_id'],'pair':pair,'messages':messages,'actions':actions,'outcome':obs['final_summary'],'source':path,'sha256':hashlib.sha256(raw).hexdigest(),'reference_label':None})
(P/'evidence.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:
 print('\nCASE',x['id'],x['pair'])
 for m in x['messages']:print(m['event'],m['actor'],m['message'])
 print('ACTIONS',[(a['event'],a['actor'],a['arguments'],a['result'].get('status')) for a in x['actions']]);print('FALLBACK',x['outcome']['random_fallback_fills'],'VIOLATIONS',x['outcome']['violations'])
