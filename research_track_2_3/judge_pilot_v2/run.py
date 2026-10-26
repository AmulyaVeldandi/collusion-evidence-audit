"""Run exactly the nine frozen v2 inputs using the existing no-retry API runner."""
import importlib.util,json,hashlib,sys
from pathlib import Path
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('pilot_v1',P.parent/'judge_pilot/run.py');api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api);api.OUT=P
m=json.loads((P/'manifest.json').read_text())
for f,key in [('instructions.txt','instructions_sha256'),('schema.json','schema_sha256')]:
 assert hashlib.sha256((P/f).read_bytes()).hexdigest()==m[key]
calls=[]
for c in m['cases']:
 data=(P/c['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==c['sha256']
 request={'model':api.MODEL,'store':False,'reasoning':{'effort':'low'},'max_output_tokens':api.MAX_OUTPUT,'instructions':(P/'instructions.txt').read_text(),'input':data.decode(),'text':{'format':{'type':'json_schema','name':'collusion_evidence_v2','strict':True,'schema':json.loads((P/'schema.json').read_text())}}}
 ident=Path(c['file']).stem;path=P/(ident+'.request.json')
 if path.exists():assert json.loads(path.read_text())==request
 else:api.dump(path,request)
 bound=(len(path.read_bytes())+4096)*.25/1e6+api.MAX_OUTPUT*2/1e6
 calls.append({'id':ident,'request_sha256':api.sha(path.read_bytes()),'max_estimated_usd':bound})
assert len(calls)==9 and sum(c['max_estimated_usd'] for c in calls)<.50
api.dump(P/'run_manifest.json',{'calls':calls,'model':api.MODEL,'spend_limit_usd':.50,'conservative_total_usd':sum(c['max_estimated_usd'] for c in calls)})
print('Prepared 9 requests; conservative USD bound',sum(c['max_estimated_usd'] for c in calls),flush=True)
if '--run' in sys.argv:api.run(calls)
