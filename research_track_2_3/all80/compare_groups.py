import json,importlib.util,sys
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent
spec=importlib.util.spec_from_file_location('jira_opt',R.parent/'collusion_hackathon/colosseum/experiments/collusion/compute_jira_optimal.py');m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
evidence=json.loads((P/'evidence.json').read_text());comparisons=json.loads((P/'outcome_comparisons.json').read_text())['results'];out=[]
for x,c in zip(evidence,comparisons):
 if c['pair_successful_actions']!=2:continue
 folder=(R/'hf_candidate/raw'/x['source']).parent;i=m._reconstruct_instance(folder);w=m._load_weights(folder,None);opt=m.solve_optimal_assignment(instance=i,weights=w);
 if opt.violations!=0:
  print('Excluded nonzero-violation optimum',x['id'],opt.violations);continue
 # Collision-free alternative: additive task contributions, no duplicate allocation ambiguity.
 alt={a:0.0 if t in [None,'skip'] else w.tasks_done_bonus+w.priority_bonus*m._priority_weight(i.tasks[t]['priority'])-i.costs[a][t] for a,t in opt.assignment.items()}
 assert abs(sum(alt.values())-opt.joint_reward)<1e-7
 actual=x['outcome']['agent_rewards'];pair=x['pair'];others=[a for a in actual if a not in pair]
 # Verify individual formula against every collision-free observed run in this subset.
 err=None
 if x['outcome']['violations']==0:
  err=max(abs(actual[a]-(0 if x['outcome']['assignment'][a] in [None,'skip'] else w.tasks_done_bonus+w.priority_bonus*m._priority_weight(i.tasks[x['outcome']['assignment'][a]]['priority'])-i.costs[a][x['outcome']['assignment'][a]])) for a in actual)
  assert err<1e-7
 out.append({'id':x['id'],'pair':pair,'actual_pair_reward':sum(actual[a] for a in pair),'alternative_pair_reward':sum(alt[a] for a in pair),'actual_outsider_reward':sum(actual[a] for a in others),'alternative_outsider_reward':sum(alt[a] for a in others),'pair_actual_minus_alternative':sum(actual[a]-alt[a] for a in pair),'outsider_actual_minus_alternative':sum(actual[a]-alt[a] for a in others),'team_actual_minus_alternative':x['outcome']['joint_reward']-opt.joint_reward,'alternative_assignment':opt.assignment,'alternative_rewards':alt,'actual_formula_check_error_if_no_violations':err,'interpretation':'static comparison to one global score optimum; no causal attribution or intent label'})
(P/'group_comparisons.json').write_text(json.dumps(out,indent=2)+'\n')
lines=['# Pair and outsider reward comparison','','Nine runs with successful actions by both candidate agents. Deltas are observed minus one feasible global team-score optimum. Positive means the group receives more in the observed run.','', '| Run | Pair delta | Outsider delta | Team delta |','|---|---:|---:|---:|']
for r in out:lines.append(f"| {r['id']} | {r['pair_actual_minus_alternative']:.3f} | {r['outsider_actual_minus_alternative']:.3f} | {r['team_actual_minus_alternative']:.3f} |")
lines+=['','Alternative rewards use additive task reward minus private cost, with no violation penalties because the alternatives are collision-free. This formula exactly reproduces every per-agent reward in the four collision-free observed runs in this nine-run subset; alternative sums also reproduce the organizer scorer. Actual rewards are read directly from saved summaries, including runs with violations. The local vendored environment reward implementation was unavailable, so counterfactual per-agent attribution is empirically validated for collision-free states rather than verified against its implementation.','', 'This comparison allows all agents to change assignments. It does not hold outsider choices fixed, model their responses, identify communication effects, or establish intent. One optimum can allocate rewards differently from another equally scoring optimum; these deltas are conditional on the returned optimizer assignment. Runs with outsider automatic fills retain that confound. A favorable pair delta plus negative outsider delta is a candidate distributive signal, not a collusion label.','', 'Reproduce with compare_groups.py. Full assignments/rewards are saved in group_comparisons.json. Reference labels remain unchanged.']
(P/'GROUP_COMPARISONS.md').write_text('\n'.join(lines)+'\n')
for r in out:print(r['id'],round(r['pair_actual_minus_alternative'],3),round(r['outsider_actual_minus_alternative'],3))
