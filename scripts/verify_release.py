"""Verify included results and frozen rules without credentials or raw logs."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'research_track_2_3'
rows=json.loads((root/'all100/scores.json').read_text())
assert len(rows)==100 and len({r['run'] for r in rows})==100
assert sum(r['corpus']=='archive80' for r in rows)==80
assert sum(r['corpus']=='fresh20' for r in rows)==20
assert len(json.loads((root/'all100/paired_differences.json').read_text()))==50
f=json.loads((root/'staged_rule/freeze_manifest.json').read_text())
for name,digest in f['sha256'].items():
 assert hashlib.sha256((root/'staged_rule'/name).read_bytes()).hexdigest()==digest,name
print('Verified100 cases,50 matched pairs and all frozen-rule hashes.')

assert len(list((root.parent/"data/test20").glob("*.json")))==20
assert not (root/"hf_candidate/raw").exists()
assert not (root/"all80/evidence.json").exists()
print("Verified20 derived test-case records; all raw source cases excluded.")
