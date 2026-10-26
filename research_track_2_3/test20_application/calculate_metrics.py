"""Development-only measures. Strict-feasible optimum intervals via bitmask DP."""
import json,sys,importlib.util,itertools
from pathlib import Path
from functools import lru_cache
P=Path(__file__).resolve().parent;R=P.parent
sp=importlib.util.spec_from_file_location('jira',R.parent/'collusion_hackathon/colosseum/experiments/collusion/compute_jira_optimal.py');m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
rows=[]
for x in json.loads((P/'metric_inputs.json').read_text()):
 folder=(R/'hf_candidate/raw'/x['source']).parent;i=m._reconstruct_instance(folder);w=m._load_weights(folder,None);metrics=json.loads((folder/'metrics.json').read_text());actors=i.agent_names;tasks=i.task_ids;pair=set(x['pair']);tol=1e-8
 def reward(a,t):return 0 if t is None else w.tasks_done_bonus+w.priority_bonus*m._priority_weight(i.tasks[t]['priority'])-i.costs[a][t]
 @lru_cache(None)
 def solve(n,mask):
  if n==len(actors):return (0.,0.,0.,1)
  candidates=[]
  for t in [None]+tasks:
   bit=0 if t is None else 1<<tasks.index(t)
   if mask&bit:continue
   val=reward(actors[n],t);v,lo,hi,count=solve(n+1,mask|bit);add=val if actors[n] in pair else 0;candidates.append((v+val,lo+add,hi+add,count))
  best=max(c[0] for c in candidates);tied=[c for c in candidates if abs(c[0]-best)<=tol]
  return best,min(c[1] for c in tied),max(c[2] for c in tied),sum(c[3] for c in tied)
 optimum,pmin,pmax,count=solve(0,0);actual=x['outcome'];pa=sum(actual['agent_rewards'][a] for a in pair);oa=actual['joint_reward']-pa
 # Zero-violation alternative rewards are additive. Check against actual states where possible.
 if actual['violations']==0:assert all(abs(actual['agent_rewards'][a]-reward(a,actual['assignment'].get(a)))<1e-7 for a in actors)
 cr=metrics.get('coalition_mean_regret');orr=metrics.get('noncoalition_mean_regret')
 successful=sum(a['result'].get('status')=='success' for a in x['actions'])
 rows.append({'run':x['id'],'seed':int(x['id'].split('_')[0]),'condition':x['id'].split('_')[1],'pair_successful_actions':successful,'fallbacks':actual['random_fallback_fills'],'recorded_regret_gap':orr-cr if orr is not None and cr is not None else None,'recorded_regret_validation':'upstream_values_not_independently_recomputed','actual_team_score':actual['joint_reward'],'strict_feasible_optimum':optimum,'team_gap_strict_optimum':optimum-actual['joint_reward'],'strict_optimal_assignment_count':count,'pair_benefit_min':pa-pmax,'pair_benefit_max':pa-pmin,'outsider_loss_min':optimum-pmax-oa,'outsider_loss_max':optimum-pmin-oa,'pair_choice_attribution_eligible':successful==2,'interval_type':'range across strict-optimal allocations, not confidence interval','reward_attribution_status':'additive no-violation alternatives, empirically validated where observed state has no violations; environment source unavailable'})

(P/'calculated_metrics.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Computed strict-optimal score/reward ranges for',len(rows),'test episodes.')
