"""Conditional automatic-fill effects; preserve successful actions, no API calls."""
import json,sys,importlib.util,csv,hashlib
from pathlib import Path
from collections import Counter
import numpy as np
from scipy.optimize import linear_sum_assignment
P=Path(__file__).resolve().parent;R=P.parent
sp=importlib.util.spec_from_file_location('jira',R.parent/'collusion_hackathon/colosseum/experiments/collusion/compute_jira_optimal.py');m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
rows=[]
for x in json.loads((P/'evidence.json').read_text()):
 folder=(R/'hf_candidate/raw'/x['source']).parent;events=json.loads((folder/'tool_events.json').read_text());i=m._reconstruct_instance(folder);w=m._load_weights(folder,None);actual=x['outcome'];fixed={}
 for e in events:
  if e['tool_name']=='assign_task' and e['result'].get('status')=='success':
   t=e['arguments'].get('task_id');fixed[e['agent_name']]=None if t in [None,'skip'] else t
 missing=[a for a in i.agent_names if a not in fixed];assert len(missing)==actual['random_fallback_fills']
 assert all(actual['assignment'].get(a) in ([None,'skip'] if t is None else [t]) for a,t in fixed.items())
 omitted={a:fixed.get(a) for a in i.agent_names};omit=m._evaluate(omitted,instance=i,weights=w);obs=m._evaluate(actual['assignment'],instance=i,weights=w);assert abs(obs.joint_reward-actual['joint_reward'])<1e-7
 best=dict(omitted);n=len(missing);occupied=Counter(t for t in fixed.values() if t is not None)
 if n:
  # Each task has n replacement slots; first is penalty-free only if no fixed actor occupies it.
  costs=np.zeros((n,n*(len(i.task_ids)+1)))
  for ai,a in enumerate(missing):
   for ti,t in enumerate(i.task_ids):
    base=w.tasks_done_bonus+w.priority_bonus*m._priority_weight(i.tasks[t]['priority'])-i.costs[a][t]
    for slot in range(n):costs[ai,ti*n+slot]=-base+(w.violation_penalty if occupied[t] or slot else 0)
  rr,cc=linear_sum_assignment(costs)
  for ai,col in zip(rr,cc):best[missing[ai]]=None if col>=n*len(i.task_ids) else i.task_ids[col//n]
 opt=m._evaluate(best,instance=i,weights=w)
 assert opt.joint_reward+1e-7>=obs.joint_reward and opt.joint_reward+1e-7>=omit.joint_reward
 row={'run':x['id'],'missing_actor_count':n,'missing_candidate_count':sum(a in x['pair'] for a in missing),'fixed_successful_choices':fixed,'recorded_fill_choices':{a:actual['assignment'][a] for a in missing},'best_replacement_choices':{a:best[a] for a in missing},'observed_score':obs.joint_reward,'score_missing_skip':omit.joint_reward,'best_score_missing_replaced':opt.joint_reward,'realized_fill_contribution_vs_skip':obs.joint_reward-omit.joint_reward,'avoidable_fill_loss_vs_best':opt.joint_reward-obs.joint_reward,'observed_violations':obs.violations,'violations_missing_skip':omit.violations,'best_replacement_violations':opt.violations,'observed_tasks':obs.tasks_done,'tasks_missing_skip':omit.tasks_done,'source_sha256':hashlib.sha256((folder/'tool_events.json').read_bytes()).hexdigest()};rows.append(row)
(P/'fill_effects.json').write_text(json.dumps(rows,indent=2)+'\n')
flat=[{k:v for k,v in r.items() if not isinstance(v,dict)} for r in rows]
with (P/'fill_effects.csv').open('w',newline='') as f:
 wri=csv.DictWriter(f,fieldnames=list(flat[0]));wri.writeheader();wri.writerows(flat)
affected=[r for r in rows if r['missing_actor_count']]
from statistics import mean
summary={'runs':len(rows),'affected_runs':len(affected),'fills_help_vs_skip':sum(r['realized_fill_contribution_vs_skip']>1e-7 for r in affected),'fills_hurt_vs_skip':sum(r['realized_fill_contribution_vs_skip']< -1e-7 for r in affected),'fills_tie_vs_skip':sum(abs(r['realized_fill_contribution_vs_skip'])<=1e-7 for r in affected),'mean_fill_contribution_affected':mean(r['realized_fill_contribution_vs_skip'] for r in affected),'mean_avoidable_fill_loss_affected':mean(r['avoidable_fill_loss_vs_best'] for r in affected),'positive_avoidable_fill_loss_runs':sum(r['avoidable_fill_loss_vs_best']>1e-7 for r in affected)}
(P/'fill_effects_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
for r in rows:
 if r['run'] in ['1_collusion','3_collusion','19_collusion','22_collusion','37_collusion']:print(r['run'],r['realized_fill_contribution_vs_skip'],r['avoidable_fill_loss_vs_best'])
