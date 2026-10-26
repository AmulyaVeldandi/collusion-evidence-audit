"""Build report tables from preserved results; no inference."""
import csv,json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1];P=Path(__file__).resolve().parent
s=json.loads((R/'judge_all80/summary.json').read_text());a=json.loads((R/'judge_all80/audit_followup.json').read_text());assert s['completed']==240 and len(a['rows'])==240
rows=[]
for view,d in s['by_view'].items():
 for category,n in d['categories'].items():rows.append({'evidence_view':view,'raw_judge_category':category,'episodes':n})
with (P/'table1_judgments.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert sum(x['episodes'] for x in rows)==240
counts=Counter(f for x in a['rows'] for f in x['evidence_policy_flags']);counts.update(f for x in a['rows'] for f in x['citation_flags'])
with (P/'table2_audit_flags.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['flag','responses_with_flag']);w.writerows(counts.most_common())
for view in ['conversation','actions_outcomes','combined']:
 ids={x['id'] for x in s['rows'] if x['view']==view};print(view,'responses',len(ids),'flagged',sum(bool(x['evidence_policy_flags'] or x['citation_flags']) for x in a['rows'] if x['id'] in ids))
