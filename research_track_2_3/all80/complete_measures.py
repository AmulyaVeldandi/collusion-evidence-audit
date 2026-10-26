"""Complete measurable corpus facts and static repair interaction. No API calls."""
import json,itertools,importlib.util,sys,hashlib,csv
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent
sp=importlib.util.spec_from_file_location('jira',R.parent/'collusion_hackathon/colosseum/experiments/collusion/compute_jira_optimal.py');m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
comparisons={x['id']:x for x in json.loads((P/'outcome_comparisons.json').read_text())['results']};agg={x['run']:x for x in json.loads((P/'aggregate_measures.json').read_text())['rows']};groups={x['id']:x for x in json.loads((P/'group_comparisons.json').read_text())};rows=[]
for x in json.loads((P/'evidence.json').read_text()):
 folder=(R/'hf_candidate/raw'/x['source']).parent;events=json.loads((folder/'tool_events.json').read_text());boards=json.loads((folder/'blackboards.json').read_text());summary=x['outcome'];i=m._reconstruct_instance(folder);w=m._load_weights(folder,None);sources={n:hashlib.sha256((folder/n).read_bytes()).hexdigest() for n in ['tool_events.json','blackboards.json','final_summary.json','metrics.json','run_config.json']}
 delivered={e['id']:(b,e) for b in boards for e in b['events'] if e.get('kind')=='communication'};posts=[]
 for n,e in enumerate(events):
  if e['tool_name']!='post_message':continue
  match=delivered.get(e['result'].get('event_id'));ok=bool(match and match[1].get('agent')==e['agent_name'] and match[1].get('payload',{}).get('content','')==e['arguments'].get('message',''))
  posts.append({'event':n,'actor':e['agent_name'],'status':'rejected' if e['result'].get('error') else 'published' if ok else 'unresolved','eligible_recipients':[a for a in match[0]['participants'] if a!=e['agent_name']] if ok else []})
 actors=[]
 for a in i.agent_names:
  calls=[(n,e) for n,e in enumerate(events) if e['agent_name']==a and e['tool_name']=='assign_task' and e['result'].get('status')=='success'];last=calls[-1][1]['arguments'].get('task_id') if calls else None
  actors.append({'actor':a,'candidate':a in x['pair'],'status':('explicit_skip' if last in [None,'skip'] else 'assigned_task') if calls else 'no_successful_action','events':[n for n,e in calls],'final_assignment':summary['assignment'].get(a)})
 actual=m._evaluate(summary['assignment'],instance=i,weights=w).joint_reward
 def repair(who):
  best=actual
  for tasks in itertools.product([None]+i.task_ids,repeat=len(who)):
   assignment=dict(summary['assignment']);assignment.update(dict(zip(who,tasks)));best=max(best,m._evaluate(assignment,instance=i,weights=w).joint_reward)
  return best-actual
 single=[repair([a]) for a in x['pair']];joint=repair(x['pair']);assert abs(joint-comparisons[x['id']]['pair_only_improvement'])<1e-7
 rewards=summary['agent_rewards'];pairmean=sum(rewards[a] for a in x['pair'])/2;others=[v for a,v in rewards.items() if a not in x['pair']];g=groups.get(x['id']);ag=agg[x['id']]
 rows.append({'run':x['id'],'successful_posts_all_agents':sum(e['status']=='published' for e in posts),'rejected_posts_all_agents':sum(e['status']=='rejected' for e in posts),'unresolved_posts_all_agents':sum(e['status']=='unresolved' for e in posts),'successful_assignments_all_agents':sum(a['status']=='assigned_task' for a in actors),'explicit_skips_all_agents':sum(a['status']=='explicit_skip' for a in actors),'missing_actions_all_agents':sum(a['status']=='no_successful_action' for a in actors),'automatic_fills_reported':summary['random_fallback_fills'],'fallback_count_reconciles':sum(a['status']=='no_successful_action' for a in actors)==summary['random_fallback_fills'],'pair_successful_actors':sum(a['status']!='no_successful_action' for a in actors if a['candidate']),'raw_mean_reward_gap':pairmean-sum(others)/len(others),'global_penalty_score_gap':comparisons[x['id']]['global_score_gap'],'strict_feasible_score_gap':ag['team_gap_strict_optimum'],'pair_repair_loss':joint,'single_actor_repair_losses':single,'joint_repair_interaction':joint-sum(single),'pair_benefit_min':ag['pair_benefit_min'],'pair_benefit_max':ag['pair_benefit_max'],'outsider_loss_min':ag['outsider_loss_min'],'outsider_loss_max':ag['outsider_loss_max'],'strict_optimal_allocation_count':ag['strict_optimal_assignment_count'],'pair_delta_one_penalty_optimum':g['pair_actual_minus_alternative'] if g else None,'outsider_delta_one_penalty_optimum':g['outsider_actual_minus_alternative'] if g else None,'recorded_regret_gap':ag['recorded_regret_gap'],'recorded_regret_status':'upstream_not_independently_recomputed','actor_records':actors,'message_records':posts,'sources_sha256':sources,'harmful_collusion_reference_label':None})
(P/'complete_measures.json').write_text(json.dumps(rows,indent=2)+'\n')
flat=[{k:v for k,v in r.items() if k not in ['actor_records','message_records','sources_sha256','single_actor_repair_losses']} for r in rows]
with (P/'complete_measures.csv').open('w',newline='') as f:
 wri=csv.DictWriter(f,fieldnames=list(flat[0]));wri.writeheader();wri.writerows(flat)
print('Runs',len(rows),'published',sum(r['successful_posts_all_agents'] for r in rows),'rejected',sum(r['rejected_posts_all_agents'] for r in rows),'unresolved',sum(r['unresolved_posts_all_agents'] for r in rows),'explicit skips',sum(r['explicit_skips_all_agents'] for r in rows),'fallback reconciliation',sum(r['fallback_count_reconciles'] for r in rows))
print('Positive joint repair interaction',sum(r['joint_repair_interaction']>1e-7 for r in rows))
