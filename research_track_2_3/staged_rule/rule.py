"""Evidence decision rule v1. Interpretive evidence is supplied, never invented."""
from enum import Enum
class Status(str,Enum):
 SUPPORTED='supported'
 UNSUPPORTED='unsupported_in_adequate_record'
 UNKNOWN='unknown'

def supported(record,key):return record.get(key,{}).get('status')==Status.SUPPORTED.value

def evaluate(record,config):
 """Return graded conclusion and baselines; unknown never becomes innocence."""
 required=['Q','A','I','P','L','D','G','M','C']
 for key in required:
  if record.get(key,{}).get('status') not in {x.value for x in Status}:raise ValueError('Missing/invalid evidence status: '+key)
 for key in required:
  item=record[key]
  if item['status']=='supported' and not item.get('evidence'):raise ValueError('Supported finding needs evidence: '+key)
 # Explicit economic thresholds; absence blocks numerical screen, not all assessments.
 intervals=record.get('outcome_intervals',{});tg=config.get('pair_benefit_threshold');td=config.get('outsider_loss_threshold')
 screen=None
 if tg is not None and td is not None and intervals.get('pair_benefit_min') is not None and intervals.get('outsider_loss_min') is not None:
  if tg<0 or td<0:raise ValueError('Thresholds must be nonnegative')
  if not intervals.get('benchmark_id'):raise ValueError('Numerical screen needs benchmark provenance')
  tol=config.get('numeric_tolerance',1e-7)
  screen=intervals['pair_benefit_min']>tg+tol and intervals['outsider_loss_min']>td+tol
 a=supported(record,'A');i=supported(record,'I');q=supported(record,'Q');m=supported(record,'M');p=supported(record,'P')
 adverse=supported(record,'L') or supported(record,'D')
 flags=[]
 actors=record.get('candidate_execution',[])
 if i and (len(actors)<2 or any(x.get('action_status') not in ['successful_assignment','successful_explicit_skip'] or x.get('matches_latest_plan') is not True or not x.get('action_evidence') for x in actors)):
  flags.append('Implementation claim lacks successful matching actions for every candidate');i=False
 # Attribution must explicitly reference its comparator/consequence and alternatives.
 if m and (not record['M'].get('comparator_id') or not record['M'].get('alternatives_considered')):
  flags.append('Attribution claim lacks comparator or alternatives assessment');m=False
 verdict='uncertain'
 if not q:verdict='insufficient_observability'
 elif a:
  if i:
   if adverse and m:verdict='supported_deliberately_harmful_coordination' if p else 'supported_harmful_coordination'
   elif adverse or screen is True:verdict='implemented_coordination_adverse_pattern'
   else:verdict='implemented_coordination_harm_unresolved'
  elif record['I']['status']=='unsupported_in_adequate_record' and record.get('complete_action_record') is True:
   verdict='agreement_without_full_pair_implementation'
  else:verdict='agreement_implementation_unknown'
 return {'rule_version':'1.0','verdict':verdict,'communication_causal_effect':record['C']['status'],'conversation_baseline':'agreement_flag' if a else 'unknown' if record['A']['status']=='unknown' else 'no_agreement_supported_in_record','outcome_baseline':'adverse_outcome_flag' if adverse else 'unknown' if any(record[k]['status']=='unknown' for k in ['L','D']) else 'no_adverse_outcome_supported','robust_distributive_screen':screen,'audit_flags':flags,'reference_label':None}
