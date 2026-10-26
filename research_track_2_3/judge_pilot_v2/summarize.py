import json
from pathlib import Path
from validate import validate
P=Path(__file__).resolve().parent
rows=[];cost=0
for p in sorted(P.glob('*.prediction.json')):
 d=json.loads(p.read_text());ident=p.name.replace('.prediction.json','');e=json.loads((P/(ident+'.json')).read_text());pred=d['prediction'];u=d['usage'];cached=u['input_tokens_details'].get('cached_tokens',0)
 cost+=((u['input_tokens']-cached)*.25+cached*.025+u['output_tokens']*2)/1e6
 rows.append({'id':ident,'category':pred['category'],'agreement':pred['reciprocal_agreement']['status'],'execution':pred['plan_execution_by_actor'],'flags':validate(pred,e)})
out={'completed':len(rows),'estimated_token_cost_usd':cost,'rows':rows}
(P/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
