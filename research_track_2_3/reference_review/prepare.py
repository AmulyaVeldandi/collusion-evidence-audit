"""Prepare development reference candidates; no inference or held-out reads."""
import json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent
refs=[];forms=[]
for x in json.loads((R/'pilot15/evidence.json').read_text()):
 raw=(R/'hf_candidate/raw'/x['source']).read_bytes();assert hashlib.sha256(raw).hexdigest()==x['sha256'];events=json.loads(raw)
 actors=[]
 for actor in x['pair']:
  success=[(n,e) for n,e in enumerate(events) if e['agent_name']==actor and e['tool_name']=='assign_task' and e['result'].get('status')=='success']
  actors.append({'actor':actor,'successful_assignment_count':len(success),'successful_event_indices':[n for n,e in success],'chosen_task':success[-1][1]['arguments'].get('task_id') if success else None,'final_assignment':x['outcome']['assignment'].get(actor),'final_state_is_agent_choice':bool(success)})
 refs.append({'run':x['id'],'reference_type':'mechanical_record_facts','source':x['source'],'sha256':x['sha256'],'actors':actors,'run_fallback_count':x['outcome']['random_fallback_fills'],'limits':'Complete recorded tool stream assumed; no intent, agreement or harm label inferred.'})
 forms.append({'run':x['id'],'reviewer_id':None,'reviewer_type':None,'prior_exposure':None,'status':'unreviewed','shared_team_commitment':{'status':'unreviewed','evidence':[]},'bilateral_agreement':{'status':'unreviewed','proposal_event':None,'revision_events':[],'acceptance_events':[]},'latest_plan_by_actor':{a:None for a in x['pair']},'implementation_by_actor':{a:{'status':'unreviewed','evidence':[]} for a in x['pair']},'adverse_outcome':{'status':'unreviewed','victim':None,'comparator':None,'evidence':[]},'action_attribution':{'status':'unreviewed','evidence':[]},'communication_causality':'not_identified','alternatives':None,'category':'unreviewed','adjudication_history':[]})
(P/'mechanical_references.json').write_text(json.dumps(refs,indent=2)+'\n')
f=P/'independent_review_template.json'
if not f.exists():f.write_text(json.dumps(forms,indent=2)+'\n')
print('15 mechanical records verified; 15 independent review forms prepared. No semantic labels fabricated.')
