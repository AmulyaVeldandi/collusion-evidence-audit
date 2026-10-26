"""Join recorded facts, calculated measures and predictions without ground-truth labels."""
import json,csv
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent
comparisons={r['id']:r for r in json.loads((R/'all80/outcome_comparisons.json').read_text())['results']};groups={r['id']:r for r in json.loads((R/'all80/group_comparisons.json').read_text())};summary={r['id']:r for r in json.loads((P/'summary.json').read_text())['rows']};out=[]
for x in json.loads((R/'all80/evidence.json').read_text()):
 key=x['id'];c=comparisons[key];g=groups.get(key);ev=json.loads((P/(key+'__combined.evidence.json')).read_text());metrics=ev['recorded_metrics'];rewards=x['outcome']['agent_rewards'];pair=x['pair'];outs=[a for a in rewards if a not in pair]
 r={'run':key,'opaque_case_id':ev['case_id'],'reference_label':None,'pair_successful_actors':c['pair_successful_actions'],'fallback_fills':c['fallback_fills'],'joint_reward':c['actual_joint_reward'],'global_score_gap':c['global_score_gap'],'pair_conditional_repair_loss':c['pair_only_improvement'],'pair_mean_reward':sum(rewards[a] for a in pair)/len(pair),'outsider_mean_reward':sum(rewards[a] for a in outs)/len(outs),'recorded_coalition_mean_regret':metrics.get('coalition_mean_regret'),'recorded_outsider_mean_regret':metrics.get('noncoalition_mean_regret'),'pair_vs_one_optimum_delta':g['pair_actual_minus_alternative'] if g else None,'outsiders_vs_one_optimum_delta':g['outsider_actual_minus_alternative'] if g else None}
 r['raw_mean_reward_gap']=r['pair_mean_reward']-r['outsider_mean_reward'];r['recorded_regret_gap']=(r['recorded_outsider_mean_regret']-r['recorded_coalition_mean_regret']) if r['recorded_coalition_mean_regret'] is not None and r['recorded_outsider_mean_regret'] is not None else None
 for v in ['conversation','actions_outcomes','combined']:
  d=summary.get(key+'__'+v)
  for field in ['category','bilateral_agreement','team_commitment','benchmark_adverse_outcome','attributable_harm','flags']:r[v+'__'+field]=d[field] if d else None
 out.append(r)
(P/'all80_results.json').write_text(json.dumps(out,indent=2)+'\n')
with (P/'all80_results.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print('Merged',len(out),'cases.')
