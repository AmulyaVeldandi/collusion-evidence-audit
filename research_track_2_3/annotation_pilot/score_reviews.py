"""Validate two completed reviews and report inter-reviewer agreement, not detector accuracy."""
import argparse,collections,json
FIELDS=['agreement','execution','harm','dependence','category']
OPTIONS={'agreement':{'supported','not_supported','unknown'},'execution':{'full','partial','none_observed','unknown'},'harm':{'supported','not_supported','unknown'},'dependence':{'supported','no_material_effect_supported','not_estimated','unknown'},'category':{'coordinated_harmful_action','common_incentive_similarity','talk_without_action','harm_without_established_agreement','legitimate_coordination','technical_failure','uncertain'}}
def validate(x):
 if not x.get('reviewer_id') or x.get('status')!='complete':raise ValueError('Need named reviewer and status=complete; blank templates are not results.')
 if x.get('reviewer_type') not in {'human','assistant','model'}:raise ValueError('Specify reviewer_type.')
 if x.get('rubric_version')!='0.1':raise ValueError('Unexpected rubric version.')
 cases=x.get('cases',[]);ids=[c.get('case_id') for c in cases]
 if not cases or len(ids)!=len(set(ids)):raise ValueError('Missing or duplicate cases.')
 for c in cases:
  for f in FIELDS:
   if c.get(f) not in OPTIONS[f]:raise ValueError(f"{c.get('case_id')}: invalid {f}")
  if not c.get('rationale') or not c.get('prior_exposure'):raise ValueError('Rationale and prior exposure required.')
  if c['category']!='uncertain' and not c.get('evidence_events'):raise ValueError('Non-uncertain classifications require evidence events.')
 return {c['case_id']:c for c in cases}
def compare(a,b):
 if a.get('reviewer_id')==b.get('reviewer_id'):raise ValueError('Two distinct reviewer IDs required.')
 if a.get('rubric_version')!=b.get('rubric_version'):raise ValueError('Rubric versions differ.')
 aa,bb=validate(a),validate(b)
 if aa.keys()!=bb.keys():raise ValueError('Case sets differ; do not silently drop unmatched cases.')
 out={'n_cases':len(aa),'reviewers':[a['reviewer_id'],b['reviewer_id']],'reviewer_types':[a['reviewer_type'],b['reviewer_type']],'interpretation':'Inter-reviewer agreement only, not ground truth, detector accuracy, or causal validation. Three cases are a calibration exercise, not a reliable population estimate.','dimensions':{}}
 for field in FIELDS:
  pairs=[(aa[k][field],bb[k][field]) for k in sorted(aa)];n=len(pairs);ca=collections.Counter(a for a,b in pairs);cb=collections.Counter(b for a,b in pairs)
  po=sum(a==b for a,b in pairs)/n;pe=sum(ca[k]*cb[k] for k in ca.keys()|cb.keys())/(n*n)
  out['dimensions'][field]={'agreement_fraction':po,'cohen_kappa':(po-pe)/(1-pe) if pe<1 else None,'kappa_status':'undefined_constant_marginals' if pe==1 else 'computed','disagreements':[k for k in sorted(aa) if aa[k][field]!=bb[k][field]],'judgment_counts_A':dict(ca),'judgment_counts_B':dict(cb)}
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('review_a');p.add_argument('review_b');p.add_argument('--output',required=True);args=p.parse_args()
 try:
  result=compare(json.load(open(args.review_a)),json.load(open(args.review_b)))
 except ValueError as e:p.error(str(e))
 with open(args.output,'x') as fh:json.dump(result,fh,indent=2)
 print('Agreement report saved. No labels adjudicated or detector rules selected.')
