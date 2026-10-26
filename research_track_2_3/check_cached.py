"""Read-only structural audit; extracts five last segments with source provenance."""
import collections, hashlib, importlib.util, json, math
from pathlib import Path
BASE = Path(__file__).resolve().parent
ROOT = BASE.parent / 'collusion_hackathon/steganographic-collusion'
spec = importlib.util.spec_from_file_location('organizer_splitter', ROOT/'scripts/split_transcript_runs.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
def digest(b): return hashlib.sha256(b).hexdigest()
selected = ['audit/pricing_duopoly/pricing_duopoly_audit_0.jsonl', 'calibration/pricing_duopoly/pricing_duopoly_audit_0.jsonl', 'audit/peer_review/peer_review_audit_0.jsonl', 'experiments/pricing_duopoly/pricing_duopoly_audit_0.jsonl', 'audit/continuous_double_auction/continuous_double_auction_audit_0.jsonl']
manifest_map = collections.defaultdict(list)
for p in (ROOT/'results').rglob('*manifest*.json'):
 try:
  obj=json.loads(p.read_text())
  for entry in obj.get('runs',[]):
   if isinstance(entry,dict) and entry.get('transcript'):
    manifest_map[entry['transcript']].append({'manifest':str(p.relative_to(ROOT)), 'entry':entry})
 except (ValueError, AttributeError): pass
unique = {}; totals = collections.Counter(); samples=[]
for p in sorted((ROOT/'results').rglob('*.jsonl')):
 if p.name.endswith('_interventions.jsonl'): continue
 numbered=[(n,l) for n,l in enumerate(p.read_text().splitlines(),1) if l.strip()]
 runs=mod.split_runs([l for _,l in numbered]); offset=0
 for i,lines in enumerate(runs,1):
  records=[json.loads(l) for l in lines]; h=digest(('\n'.join(lines)+'\n').encode()); start=offset;offset+=len(lines)
  rounds=collections.defaultdict(list)
  for r in records:rounds[r['round_id']].append(r['agent_id'])
  agents=sorted({r['agent_id'] for r in records}); ids=sorted(rounds)
  issues=[]
  if ids != list(range(1,max(ids)+1)):issues.append('round_gaps_or_nonone_start')
  if any(sorted(v)!=agents for v in rounds.values()):issues.append('inconsistent_or_duplicate_agent_coverage')
  if len({r['run_id'] for r in records})!=1:issues.append('mixed_run_ids')
  if any(not isinstance(r['reward'],(float,int)) or not math.isfinite(r['reward']) for r in records):issues.append('invalid_reward')
  na=sum(r['action']=='n/a' for r in records)
  numeric_bad=0
  if 'pricing_duopoly' in str(p) or 'auction' in str(p):
   for r in records:
    try:float(r['action'])
    except (ValueError,TypeError):numeric_bad+=1
  info={'sha256':h,'records':len(records),'rounds':len(ids),'agents':agents,'structural_issues':issues,'n_a_actions':na,'nonnumeric_market_actions':numeric_bad}
  if h not in unique:unique[h]=info
  if str(p.relative_to(ROOT/'results')) in selected and i==len(runs):
   refs=manifest_map[str(p.relative_to(ROOT))]
   companion=p.with_name(p.stem+'_interventions.jsonl')
   companion_match=None
   if companion.exists():
    c=[json.loads(l) for l in companion.read_text().splitlines() if l.strip()]
    lookup={x['round']:x['interventions'] for x in c}
    companion_match=len(c)==len(ids) and all(lookup.get(r['round_id'],{}).get(r['role'])==r['interventions'] for r in records)
   sums={a:sum(r['reward'] for r in records if r['agent_id']==a) for a in agents}
   item={**info,'source':str(p.relative_to(ROOT)),'source_sha256':digest(p.read_bytes()),'segment':i,'segments_in_file':len(runs),'source_lines':[numbered[start][0],numbered[offset-1][0]],'manifest_candidates':refs,'companion_matches_row_interventions':companion_match,'reward_sums':sums,'reference_label':'unadjudicated'}
   out=BASE/'cached_samples';out.mkdir(exist_ok=True)
   name=str(p.relative_to(ROOT/'results')).replace('/','__')
   (out/name).write_text('\n'.join(lines)+'\n');item['extracted_file']=str((out/name).relative_to(BASE));samples.append(item)
  totals['segments']+=1
 totals['files']+=1
summary={'files':totals['files'],'segments':totals['segments'],'byte_unique_segments':len(unique),'unique_segments_with_structural_issues':sum(bool(v['structural_issues']) for v in unique.values()),'unique_segments_with_na_actions':sum(v['n_a_actions']>0 for v in unique.values()),'unique_segments_with_nonnumeric_market_actions':sum(v['nonnumeric_market_actions']>0 for v in unique.values()),'agent_counts_unique_segments':dict(collections.Counter(len(v['agents']) for v in unique.values())),'note':'Structural completeness does not establish expected episode length, provenance, agent independence, or valid research labels.'}
(BASE/'cached_check.json').write_text(json.dumps({'summary':summary,'samples':samples},indent=2)+'\n')
print(json.dumps(summary,indent=2))
for s in samples: print(json.dumps(s,indent=2))
manifest_audit=[]
for e in json.loads((ROOT/'results/dataset_manifest.json').read_text()).get('runs',[]):
 p=ROOT/e['transcript']
 status='missing' if not p.exists() else ('match' if digest(p.read_bytes())==e.get('transcript_sha256') else 'hash_mismatch')
 manifest_audit.append({'source':e['transcript'],'status':status})
(BASE/'cached_manifest_check.json').write_text(json.dumps({'counts':dict(collections.Counter(x['status'] for x in manifest_audit)), 'entries':manifest_audit},indent=2)+'\n')
