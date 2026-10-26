import json,sys
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'judge_pilot_v3'));from validate import validate
rows=[];cost=0
for p in sorted(P.glob('*.prediction.json')):
 ident=p.name.replace('.prediction.json','');d=json.loads(p.read_text());e=json.loads((P/(ident+'.evidence.json')).read_text());u=d['usage'];cached=u['input_tokens_details'].get('cached_tokens',0);cost+=((u['input_tokens']-cached)*.25+cached*.025+u['output_tokens']*2)/1e6
 rows.append({'id':ident,'category':d['prediction']['category'],'agreement':d['prediction']['reciprocal_agreement']['status'],'flags':validate(d['prediction'],e)})
result={'completed':len(rows),'estimated_cost_usd':cost,'flagged_responses':sum(bool(r['flags']) for r in rows),'rows':rows};(P/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
