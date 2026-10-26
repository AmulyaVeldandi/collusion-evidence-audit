"""Deterministic publication/access audit; no inference calls or held-out reads."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
rows={r['trajectory_id']:r for r in map(json.loads,(ROOT/'hf_candidate/prepared/development.jsonl').read_text().splitlines())}
out=[]
for m in json.loads((ROOT/'annotation_pilot/source_key_DO_NOT_SHARE_WITH_REVIEWERS.json').read_text()):
 r=rows[m['trajectory_id']];files=r['provenance']['files_sha256'];names=m['names']
 def read(suffix):
  path=next(k for k in files if k.endswith('/'+suffix));b=(ROOT/'hf_candidate/raw'/path).read_bytes()
  assert hashlib.sha256(b).hexdigest()==files[path]
  return json.loads(b),{'path':path,'sha256':files[path]}
 events,es=read('tool_events.json');boards,bs=read('blackboards.json')
 messages=[]
 for i,e in enumerate(events):
  if e['tool_name']!='post_message':continue
  result=e['result'];eid=result.get('event_id');matches=[(b,x) for b in boards for x in b['events'] if eid and x.get('id')==eid and x.get('kind')=='communication']
  matched=len(matches)==1
  consistent=matched and matches[0][1].get('agent')==e['agent_name'] and matches[0][1].get('payload',{}).get('content')==e['arguments'].get('message')
  status='rejected' if result.get('error') else 'published' if consistent else 'unresolved'
  board=matches[0][0] if consistent else None
  messages.append({'tool_event_index':i,'sender':names[e['agent_name']],'event_id':eid,'publication_status':status,'board_id':board['blackboard_id'] if board else None,'eligible_other_participants':[names[a] for a in board['participants'] if a!=e['agent_name']] if board else [],'recipient_model_input_verified':False,'specific_acknowledgment':'not_assessed','behavioral_influence':'not_estimated'})
 out.append({'case_id':m['case_id'],'sources':[es,bs],'counts':{s:sum(x['publication_status']==s for x in messages) for s in ['published','rejected','unresolved']},'messages':messages})
path=ROOT/'judge_pilot/communication_audit.json';path.write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(x['case_id'],x['counts'])
