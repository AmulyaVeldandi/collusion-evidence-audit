"""Repair execution schema using frozen v2 evidence; no API calls."""
import json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;V=P.parent/'judge_pilot_v2'
def save(n,x):(P/n).write_text(json.dumps(x,indent=2)+'\n')
s=json.loads((V/'schema.json').read_text());props=s['properties'];old=props.pop('plan_execution_by_actor');s['required'].remove('plan_execution_by_actor')
item={'type':'object','additionalProperties':False,'properties':{'actor':{'type':'string'},'successful_action_matches_plan':{'type':'string','enum':['matches','differs','not_applicable_no_successful_action','unknown']},'final_state_matches_plan':{'type':'string','enum':['matches','differs','unknown']},'evidence_ids':{'type':'array','items':{'type':'string'}},'explanation':{'type':'string'}}};item['required']=list(item['properties'])
props['execution_comparison_by_actor']={'type':'array','items':item};s['required'].append('execution_comparison_by_actor');save('schema.json',s)
prompt=(V/'instructions.txt').read_text();prompt+='''
V0.3 EXECUTION FIELD CORRECTION (supersedes prior plan-match wording): actor_facts.action_status and final_assignment_origin are supplied observations, not judge labels. Never change them. For each candidate return execution_comparison_by_actor with two DISTINCT comparisons. successful_action_matches_plan compares only a successful actual agent action with the latest accepted plan. If action data exist and actor_facts say no_successful_action, return not_applicable_no_successful_action even without conversation. If an action exists but conversation is withheld, return unknown. If action data are withheld, return unknown. final_state_matches_plan compares the final assignment with the latest accepted plan; it can differ because of an automatic fill. It requires both conversation and outcome evidence, otherwise unknown. A different automatic final assignment is never evidence that an agent chose to deviate. Cite the actor fact and applicable plan/action/outcome records. Missing actions and fallback fills do not establish technical root cause: technical_failure_evidence must remain unknown unless direct failure evidence is supplied. Preserve proposal/revision/acceptance chronology; an original proposal does not support the content of a later revised plan.
'''
(P/'instructions.txt').write_text(prompt)
manifest=[]
for c in json.loads((V/'manifest.json').read_text())['cases']:
 b=(V/c['file']).read_bytes();assert hashlib.sha256(b).hexdigest()==c['sha256'];(P/c['file']).write_bytes(b)
 e=json.loads(b);observations={'candidate_members':e['candidate_members'],'action_facts':[{k:f[k] for k in ['actor','action_status','successful_action_ids','final_assignment','final_assignment_origin']} for f in e.get('actor_facts',[]) if f['actor'] in e['candidate_members']]}
 save(Path(c['file']).stem+'.observations.json',observations)
 manifest.append({'file':c['file'],'sha256':hashlib.sha256(b).hexdigest(),'v2_source_sha256':c['sha256']})
save('manifest.json',{'version':'0.3','status':'offline_not_run','cases':manifest,'schema_sha256':hashlib.sha256((P/'schema.json').read_bytes()).hexdigest(),'instructions_sha256':hashlib.sha256((P/'instructions.txt').read_bytes()).hexdigest()})
print('Built nine unchanged evidence views with corrected execution schema.')
