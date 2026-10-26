"""Summarize saved predictions only; never call API or label ground truth."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
rows=[];cost=0
for p in sorted(P.glob('*.prediction.json')):
 d=json.loads(p.read_text());pred=d['prediction']; req=json.loads((P/(p.name.replace('.prediction.json','.request.json'))).read_text());ev=json.loads(req['input'])
 ids={x['id'] for k in ['channels','delivered_messages','action_tool_events'] for x in ev.get(k,[])}
 if 'outcome' in ev:ids.add(ev['outcome']['id'])
 invalid=[eid for k in ['agreement','delivery','execution','harm','coalition_benefit','behavioral_dependence'] for eid in pred[k]['evidence_ids'] if eid not in ids]
 u=d['usage'];cached=u['input_tokens_details'].get('cached_tokens',0)
 c=((u['input_tokens']-cached)*.25+cached*.025+u['output_tokens']*2)/1e6;cost+=c
 rows.append({'id':p.name.replace('.prediction.json',''),'category':pred['category'],'agreement':pred['agreement']['status'],'execution':pred['execution']['status'],'harm':pred['harm']['status'],'dependence':pred['behavioral_dependence']['status'],'invalid_citations':invalid,'estimated_usd':c})
result={'completed':len(rows),'estimated_cost_usd':cost,'cost_basis':'published token rates, not invoice','rows':rows}
(P/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
