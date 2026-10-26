"""Post hoc checks of existing100-case scores. No inference or new experiments."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent
rows=json.loads((R/'all100/scores.json').read_text());tol=1e-7
identity={side:max(abs(r['outsider_loss_'+side]-r['strict_feasible_score_gap']-r['pair_benefit_'+side]) for r in rows) for side in ['min','max']}
assert max(identity.values())<tol
summary={'episodes':len(rows),'max_identity_residual':identity,'identity':'outsider_loss_bound = team_gap + pair_benefit_bound, for the same strict-optimal benchmark','corpora':{}}
for corpus in ['archive80','fresh20']:
 x=[r for r in rows if r['corpus']==corpus];full=[r for r in x if r['pair_successful_actors']==2];rob=lambda r:r['pair_benefit_min']>tol and r['outsider_loss_min']>tol
 summary['corpora'][corpus]={'episodes':len(x),'positive_team_gap':sum(r['strict_feasible_score_gap']>tol for r in x),'raw_reward_gap_positive':sum(r['raw_mean_reward_gap']>tol for r in x),'raw_positive_without_robust_pattern':sum(r['raw_mean_reward_gap']>tol and not rob(r) for r in x),'robust_pattern':sum(rob(r) for r in x),'robust_pattern_without_raw_positive':sum(rob(r) and r['raw_mean_reward_gap']<=tol for r in x),'full_pair_execution':len(full),'full_execution_gap_positive_pair_repair_zero':sum(r['strict_feasible_score_gap']>tol and abs(r['pair_repair_loss'])<=tol for r in full),'screen_equals_pair_benefit_test':all(rob(r)==(r['pair_benefit_min']>tol) for r in x)}
(P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
