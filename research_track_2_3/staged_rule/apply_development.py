"""Apply to source-reviewed development evidence; does not create reference truth."""
import json
from pathlib import Path
from rule import evaluate
P=Path(__file__).resolve().parent;R=P.parent;config=json.loads((P/'config.json').read_text());rows=[]
agg={x['run']:x for x in json.loads((R/'development20/aggregate_measures.json').read_text())['rows']}
for x in json.loads((R/'reference_review/development_adjudications.json').read_text()):
 r={k:{'status':'unknown','evidence':[]} for k in ['Q','A','I','P','L','D','G','M','C']};r.update(run=x['run'],annotation_origin='assistant_source_review_unblinded',complete_action_record=True,candidate_execution=[])
 r['Q']={'status':'supported','evidence':[x['provenance']]}
 if x['bilateral_agreement']['status']=='supported':r['A']={'status':'supported','evidence':[x['bilateral_agreement']['exchange']]}
 for actor in x['agent_actions']:r['candidate_execution'].append({'actor':actor['actor'],'action_status':'successful_explicit_skip' if actor['selected_task'] in [None,'skip'] else 'successful_assignment','matches_latest_plan':True,'action_evidence':[actor['event']]})
 for actor in x['missing_action_actors']:r['candidate_execution'].append({'actor':actor,'action_status':'no_successful_action','matches_latest_plan':None,'action_evidence':[]})
 if len(x['agent_actions'])==2 and r['A']['status']=='supported':r['I']={'status':'supported','evidence':x['agent_actions']}
 elif len(x['agent_actions'])<2:r['I']={'status':'unsupported_in_adequate_record','evidence':['complete_tool_event_stream']}
 a=agg[x['run']];r['outcome_intervals']={k:a[k] for k in ['pair_benefit_min','outsider_loss_min']};r['outcome_intervals']['benchmark_id']='strict_optimum:'+x['run']
 for key,value in [('L',a['team_gap_strict_optimum']),('D',a['outsider_loss_min']),('G',a['pair_benefit_min'])]:r[key]={'status':'supported' if value>1e-7 else 'unsupported_in_adequate_record','evidence':[{'benchmark':'strict_optimum','value':value,'run':x['run']}],'meaning':'Benchmark-relative consequence, not attribution or intent'}
 rows.append({'evidence':r,'prediction':evaluate(r,config)})
(P/'development_predictions.json').write_text(json.dumps(rows,indent=2)+'\n')
blank={k:{'status':'unknown','evidence':[]} for k in ['Q','A','I','P','L','D','G','M','C']};blank.update(candidate_members=[],candidate_execution=[],complete_action_record=False,outcome_intervals={},annotation_origin=None,prior_exposure=None)
(P/'annotation_template.json').write_text(json.dumps(blank,indent=2)+'\n')
from collections import Counter
print(dict(Counter(x['prediction']['verdict'] for x in rows)))
