"""Reuse organizer Jira scorer; static counterfactuals, never causal labels."""
import json,importlib.util,sys,hashlib,itertools,math
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent
source=R.parent/'collusion_hackathon/colosseum/experiments/collusion/compute_jira_optimal.py'
spec=importlib.util.spec_from_file_location('jira_opt',source);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
rows=[]
for x in json.loads((P/'evidence.json').read_text()):
 folder=(R/'hf_candidate/raw'/x['source']).parent;summary=x['outcome'];weights=mod._load_weights(folder,None);prompt=mod._load_instance_from_agent_prompts(folder);instance=mod._reconstruct_instance(folder)
 # Validate reconstructed private costs against logged rounded tables, not merely outcome totals.
 costerr=max(abs(instance.costs[a][t]-prompt.costs[a][t]) for a in instance.agent_names for t in instance.task_ids)
 assert costerr<=.005001,(x['id'],costerr)
 assert instance.tasks==prompt.tasks or all(instance.tasks[t]['priority']==prompt.tasks[t]['priority'] and instance.tasks[t]['effort']==prompt.tasks[t]['effort'] for t in instance.task_ids)
 actual=mod._evaluate(summary['assignment'],instance=instance,weights=weights)
 assert abs(actual.joint_reward-summary['joint_reward'])<1e-7,(x['id'],actual.joint_reward,summary['joint_reward'])
 assert actual.violations==summary['violations']
 optimal=mod.solve_optimal_assignment(instance=instance,weights=weights)
 saved=json.loads((folder/'optimal_summary.json').read_text())
 assert abs(saved['optimal']['joint_reward']-optimal.joint_reward)<1e-7
 acts={a['actor']:a for a in x['actions'] if a['result'].get('status')=='success'}
 for actor,a in acts.items():assert (a['arguments'].get('task_id') if a['arguments'].get('task_id')!='skip' else None)==summary['assignment'][actor]
 best=actual;best_unique=None
 for choices in itertools.product([None]+instance.task_ids,repeat=2):
  assignment=dict(summary['assignment']);assignment.update(dict(zip(x['pair'],choices)))
  candidate=mod._evaluate(assignment,instance=instance,weights=weights)
  if candidate.joint_reward>best.joint_reward+1e-9:best=candidate
  if candidate.violations==0 and (best_unique is None or candidate.joint_reward>best_unique.joint_reward):best_unique=candidate
 rows.append({'id':x['id'],'pair':x['pair'],'pair_successful_actions':len(acts),'fallback_fills':summary['random_fallback_fills'],'actual_joint_reward':actual.joint_reward,'global_score_optimum':optimal.joint_reward,'global_score_gap':optimal.joint_reward-actual.joint_reward,'global_optimum_violations':optimal.violations,'pair_only_best_reward_fixed_others':best.joint_reward,'pair_only_improvement':best.joint_reward-actual.joint_reward,'pair_only_best_assignment':best.assignment,'pair_only_best_violations':best.violations,'pair_only_best_zero_violation_reward':best_unique.joint_reward if best_unique else None,'eligible_for_pair_choice_interpretation':len(acts)==2,'interpretation':'static opportunity cost, not causal collusion harm; missing pair actions exclude pair choice attribution','max_cost_rounding_error':costerr,'files_sha256':{name:hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in ['agent_prompts.json','run_config.json','final_summary.json','optimal_summary.json']}})
(P/'outcome_comparisons.json').write_text(json.dumps({'scorer_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'results':rows},indent=2)+'\n')
for r in rows:print(r['id'],'pair_actions',r['pair_successful_actions'],'global_gap',round(r['global_score_gap'],3),'pair_gain',round(r['pair_only_improvement'],3),'opt_violations',r['global_optimum_violations'])
