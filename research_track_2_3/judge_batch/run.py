"""Remaining twelve development cases, three views each; no retries."""
import json,re,hashlib,importlib.util,sys
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent
sp=importlib.util.spec_from_file_location('api_runner',R/'judge_pilot/run.py');api=importlib.util.module_from_spec(sp);sp.loader.exec_module(api);api.OUT=P
instructions=(R/'judge_pilot_v3/instructions.txt').read_text();schema=json.loads((R/'judge_pilot_v3/schema.json').read_text());calls=[]
for x in json.loads((R/'pilot15/evidence.json').read_text()):
 if x['id'] in ['1_baseline','1_collusion','3_collusion']:continue
 folder=(R/'hf_candidate/raw'/x['source']).parent
 events=json.loads((folder/'tool_events.json').read_text());assert hashlib.sha256((folder/'tool_events.json').read_bytes()).hexdigest()==x['sha256']
 boards=json.loads((folder/'blackboards.json').read_text());final=x['outcome'];names={a:'Agent '+str(n+1) for n,a in enumerate(sorted(final['agent_rewards']))};pair=sorted(names[a] for a in x['pair']);pat=re.compile(r'\b(?:'+'|'.join(re.escape(a) for a in sorted(names,key=len,reverse=True))+r')\b')
 def anon(o):return json.loads(pat.sub(lambda m:names[m.group()],json.dumps(o)))
 delivered={e['id']:b for b in boards for e in b['events'] if e.get('kind')=='communication'};messages=[];comm=[];actions=[]
 for idx,e in enumerate(events):
  eid='event_'+str(idx)
  if e['tool_name']=='post_message':
   b=delivered.get(e['result'].get('event_id'));ok=b is not None and not e['result'].get('error')
   if ok:
    match=next(t for t in b['events'] if t['id']==e['result']['event_id']);assert match['agent']==e['agent_name'] and match['payload']['content']==e['arguments']['message']
    messages.append({'id':eid,'actor':e['agent_name'],'board':b['blackboard_id'],'message':e['arguments']['message']})
   comm.append({'tool_event_index':idx,'sender':e['agent_name'],'publication_status':'published' if ok else 'rejected' if e['result'].get('error') else 'unresolved','eligible_other_participants':[a for a in b['participants'] if a!=e['agent_name']] if ok else [],'recipient_model_input_verified':False})
  else:actions.append({'id':eid,'actor':e['agent_name'],'tool':e['tool_name'],'arguments':e['arguments'],'result':e['result']})
 facts=[]
 for a in sorted(names):
  success=[e for e in actions if e['actor']==a and e['tool']=='assign_task' and e['result'].get('status')=='success'];task=success[-1]['arguments'].get('task_id') if success else None
  facts.append({'id':'actor_'+names[a].replace(' ','_'),'actor':a,'successful_action_ids':[e['id'] for e in success],'action_status':('explicit_skip' if task in [None,'skip'] else 'assigned_task') if success else 'no_successful_action','selected_task':task,'final_assignment':final['assignment'].get(a),'final_assignment_origin':'agent_tool' if success else 'unresolved'})
 missing=[f for f in facts if f['action_status']=='no_successful_action']
 if len(missing)==final['random_fallback_fills']:
  for f in missing:f['final_assignment_origin']='automatic_fill_inferred_from_complete_log_and_count'
 for view in ['conversation','actions_outcomes','combined']:
  ev={'case_id':x['id'],'view':view,'candidate_members':pair,'evidence_availability':{'conversation':view!='actions_outcomes','actions_outcomes':view!='conversation','recipient_input_exposure':False,'harm_comparator':False,'independence_control':False,'causal_intervention':False}}
  if view!='actions_outcomes':ev.update(channels=[{'id':'board_'+str(b['blackboard_id']),'participants':b['participants']} for b in boards],delivered_messages=messages,communication_facts=comm)
  if view!='conversation':ev.update(action_tool_events=actions,outcome={'id':'final_summary','data':final},actor_facts=facts)
  ev=anon(ev);ident=x['id']+'__'+view;api.dump(P/(ident+'.evidence.json'),ev)
  req={'model':api.MODEL,'store':False,'reasoning':{'effort':'low'},'max_output_tokens':6000,'instructions':instructions,'input':json.dumps(ev),'text':{'format':{'type':'json_schema','name':'collusion_evidence_v3','strict':True,'schema':schema}}}
  dest=P/(ident+'.request.json')
  if dest.exists():assert json.loads(dest.read_text())==req
  else:api.dump(dest,req)
  calls.append({'id':ident,'request_sha256':api.sha(dest.read_bytes()),'source_sha256':x['sha256'],'max_estimated_usd':(len(dest.read_bytes())+4096)*.25/1e6+.012})
assert len(calls)==36 and sum(c['max_estimated_usd'] for c in calls)<1.50
api.dump(P/'manifest.json',{'calls':calls,'spend_ceiling_usd':1.50,'conservative_bound_usd':sum(c['max_estimated_usd'] for c in calls),'instructions_sha256':api.sha(instructions.encode()),'schema_sha256':api.sha(json.dumps(schema).encode())})
print('36 calls; conservative bound USD',sum(c['max_estimated_usd'] for c in calls),flush=True)
if '--run' in sys.argv:
 from concurrent.futures import ThreadPoolExecutor
 with ThreadPoolExecutor(max_workers=3) as pool:
  futures=[pool.submit(api.run,calls[i::3]) for i in range(3)]
  for f in futures:
   try:f.result()
   except Exception as error:print('Worker stopped; uncertain attempts require inspection:',type(error).__name__,flush=True)
