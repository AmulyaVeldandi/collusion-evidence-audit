"""Remaining twelve development cases, three views each; no retries."""
import json,re,hashlib,importlib.util,sys
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent
sp=importlib.util.spec_from_file_location('api_runner',R/'judge_pilot/run.py');api=importlib.util.module_from_spec(sp);sp.loader.exec_module(api);api.OUT=P
comparisons={x['id']:x for x in json.loads((R/'all80/outcome_comparisons.json').read_text())['results']}
instructions=(P/'instructions.txt').read_text();schema=json.loads((P/'schema.json').read_text());calls=[]
for x in json.loads((R/'all80/evidence.json').read_text()):
 folder=(R/'hf_candidate/raw'/x['source']).parent
 events=json.loads((folder/'tool_events.json').read_text());assert hashlib.sha256((folder/'tool_events.json').read_bytes()).hexdigest()==x['sha256']
 prompts=json.loads((folder/'agent_prompts.json').read_text());recorded=json.loads((folder/'metrics.json').read_text())
 boards=json.loads((folder/'blackboards.json').read_text());final=x['outcome'];names={a:'Agent '+str(n+1) for n,a in enumerate(sorted(final['agent_rewards']))};pair=sorted(names[a] for a in x['pair']);pat=re.compile(r'\b(?:'+'|'.join(re.escape(a) for a in sorted(names,key=len,reverse=True))+r')\b')
 def anon(o):return json.loads(pat.sub(lambda m:names[m.group()],json.dumps(o)))
 delivered={e['id']:b for b in boards for e in b['events'] if e.get('kind')=='communication'};messages=[];comm=[];actions=[]
 for idx,e in enumerate(events):
  eid='event_'+str(idx)
  if e['tool_name']=='post_message':
   b=delivered.get(e['result'].get('event_id'));ok=b is not None and not e['result'].get('error')
   if ok:
    match=next(t for t in b['events'] if t['id']==e['result']['event_id']);assert match['agent']==e['agent_name'] and match['payload']['content']==e['arguments'].get('message','')
    messages.append({'id':eid,'actor':e['agent_name'],'board':b['blackboard_id'],'message':e['arguments'].get('message','')})
   comm.append({'tool_event_index':idx,'sender':e['agent_name'],'publication_status':'published' if ok else 'rejected' if e['result'].get('error') else 'unresolved','eligible_other_participants':[a for a in b['participants'] if a!=e['agent_name']] if ok else [],'recorded_recipient_input_inclusion':{a:bool(ok and e['arguments'].get('message','') and any(p.get('agent_name')==a and e['arguments'].get('message','') in p.get('user_prompt','') for p in prompts)) for a in x['pair'] if a!=e['agent_name']},'provider_payload_verified':False})
  else:actions.append({'id':eid,'actor':e['agent_name'],'tool':e['tool_name'],'arguments':e['arguments'],'result':e['result']})
 facts=[]
 for a in sorted(names):
  success=[e for e in actions if e['actor']==a and e['tool']=='assign_task' and e['result'].get('status')=='success'];task=success[-1]['arguments'].get('task_id') if success else None
  facts.append({'id':'actor_'+names[a].replace(' ','_'),'actor':a,'successful_action_ids':[e['id'] for e in success],'action_status':('explicit_skip' if task in [None,'skip'] else 'assigned_task') if success else 'no_successful_action','selected_task':task,'final_assignment':final['assignment'].get(a),'final_assignment_origin':'agent_tool' if success else 'unresolved'})
 missing=[f for f in facts if f['action_status']=='no_successful_action']
 if len(missing)==final['random_fallback_fills']:
  for f in missing:f['final_assignment_origin']='automatic_fill_inferred_from_complete_log_and_count'
 for view in ['conversation','actions_outcomes','combined']:
  ev={'case_id':hashlib.sha256(x['trajectory_id'].encode()).hexdigest()[:16],'view':view,'candidate_members':pair,'evidence_availability':{'conversation':view!='actions_outcomes','actions_outcomes':view!='conversation','recipient_input_exposure':view!='actions_outcomes','harm_comparator':view!='conversation','independence_control':False,'causal_intervention':False}}
  if view!='actions_outcomes':ev.update(channels=[{'id':'board_'+str(b['blackboard_id']),'participants':b['participants']} for b in boards],delivered_messages=messages,communication_facts=comm)
  if view!='conversation':ev.update(action_tool_events=actions,outcome={'id':'final_summary','data':final},actor_facts=facts)
  if view!='conversation':
   ev['computed_comparisons']={'id':'computed_comparisons',**{k:v for k,v in comparisons[x['id']].items() if k not in ['id','files_sha256','max_cost_rounding_error']}}
   ev['recorded_metrics']={'id':'recorded_metrics',**{k:recorded.get(k) for k in ['coalition_mean_regret','noncoalition_mean_regret','coalition_mean_reward','noncoalition_mean_reward','reward_std','noncoalition_reward_std']},'provenance':'upstream_recorded_not_independently_recomputed'}
  ev=anon(ev);ident=x['id']+'__'+view;api.dump(P/(ident+'.evidence.json'),ev)
  req={'model':api.MODEL,'store':False,'reasoning':{'effort':'low'},'max_output_tokens':6000,'instructions':instructions,'input':json.dumps(ev),'text':{'format':{'type':'json_schema','name':'collusion_evidence_v4','strict':True,'schema':schema}}}
  dest=P/(ident+'.request.json')
  if dest.exists():assert json.loads(dest.read_text())==req
  else:api.dump(dest,req)
  calls.append({'id':ident,'request_sha256':api.sha(dest.read_bytes()),'source_sha256':x['sha256'],'max_estimated_usd':(len(dest.read_bytes())+4096)*.25/1e6+.012})
assert len(calls)==240 and sum(c['max_estimated_usd'] for c in calls)<8.00
api.dump(P/'manifest.json',{'calls':calls,'spend_ceiling_usd':8.00,'conservative_bound_usd':sum(c['max_estimated_usd'] for c in calls),'instructions_sha256':api.sha(instructions.encode()),'schema_sha256':api.sha(json.dumps(schema).encode())})
print('240 calls; conservative bound USD',sum(c['max_estimated_usd'] for c in calls),flush=True)
if '--run' in sys.argv:
 from concurrent.futures import ThreadPoolExecutor,as_completed
 def execute(c):
  try:api.run([c])
  except Exception as error:
   api.dump(P/(c['id']+'.transport_error.json'),{'error_type':type(error).__name__,'delivery_status':'unknown','retried':False})
   print('Request stopped:',c['id'],type(error).__name__,flush=True)
 with ThreadPoolExecutor(max_workers=6) as pool:
  futures=[pool.submit(execute,c) for c in calls]
  for f in as_completed(futures):f.result()
