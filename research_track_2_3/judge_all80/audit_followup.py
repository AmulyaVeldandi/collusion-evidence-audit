import json,re
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parent;s=json.loads((P/'summary.json').read_text());out=[]
for row in s['rows']:
 ident=row['id'];p=json.loads((P/(ident+'.prediction.json')).read_text())['prediction'];e=json.loads((P/(ident+'.evidence.json')).read_text());original=row['flags'];semantic=[f for f in original if not f.endswith(':invalid_citation')];citation=[f for f in original if f.endswith(':invalid_citation')]
 ids={t['id'] for k in ['channels','delivered_messages','action_tool_events','actor_facts'] for t in e.get(k,[])}|{k for k in ['computed_comparisons','recorded_metrics'] if k in e}
 if 'outcome' in e:ids.add('final_summary')
 defects=[]
 for k,v in p.items():
  for item in v if isinstance(v,list) else [v]:
   if isinstance(item,dict):
    for c in item.get('evidence_ids',[]):
     if c not in ids: defects.append({'field':k,'citation':c,'formatting_only_candidate':bool(re.fullmatch('event[0-9]+',c) and c.replace('event','event_',1) in ids)})
 facts={t['actor']:t for t in e.get('actor_facts',[])}
 if p['category'] in ['supported_harmful_coordination','coordinated_action_adverse_pattern','implemented_coordination_harm_unresolved']:
  if e['view']!='combined':semantic.append('category:implementation_not_observable')
  elif any(facts[a]['action_status']=='no_successful_action' for a in e['candidate_members']):semantic.append('category:full_pair_execution_missing')
 out.append({'id':ident,'evidence_policy_flags':semantic,'citation_flags':citation,'citation_defects':defects,'note':'Policy flags require semantic review; negative-in-record versus unknown can be a coding-convention mismatch. Citation existence is not content support.'})
summary={'responses':len(out),'evidence_policy_flagged':sum(bool(x['evidence_policy_flags']) for x in out),'citation_flagged':sum(bool(x['citation_flags']) for x in out),'citation_only_responses':sum(bool(x['citation_flags']) and not x['evidence_policy_flags'] for x in out),'rows':out}
(P/'audit_followup.json').write_text(json.dumps(summary,indent=2)+'\n');print({k:v for k,v in summary.items() if k!='rows'})
