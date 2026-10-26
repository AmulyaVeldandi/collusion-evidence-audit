"""Execution semantic checks, with all other v2 checks retained."""
import importlib.util
from pathlib import Path
sp=importlib.util.spec_from_file_location('v2_checks',Path(__file__).resolve().parents[1]/'judge_pilot_v2/validate.py');v2=importlib.util.module_from_spec(sp);sp.loader.exec_module(v2)
def validate(pred,ev):
 # Reuse non-execution checks without pretending new output was an old prediction.
 legacy=dict(pred);legacy['plan_execution_by_actor']=[{'actor':a,'match':'unknown','evidence_ids':[]} for a in ev['candidate_members']]
 errors=v2.validate(legacy,ev)
 entries=pred['execution_comparison_by_actor'];available=ev['evidence_availability'];facts={f['actor']:f for f in ev.get('actor_facts',[])}
 if sorted(x['actor'] for x in entries)!=sorted(ev['candidate_members']):errors.append('execution:wrong_actors')
 ids={x['id'] for k in ['delivered_messages','action_tool_events','actor_facts'] for x in ev.get(k,[])}
 if 'outcome' in ev:ids.add('final_summary')
 for x in entries:
  if any(i not in ids for i in x['evidence_ids']):errors.append('execution:invalid_citation')
  f=facts.get(x['actor']);a=x['successful_action_matches_plan'];final=x['final_state_matches_plan']
  if not available['actions_outcomes']:
   if a!='unknown':errors.append('execution:actions_withheld')
  elif f and f['action_status']=='no_successful_action':
   if a!='not_applicable_no_successful_action':errors.append('execution:no_agent_action')
  elif not available['conversation'] and a!='unknown':errors.append('execution:plan_withheld')
  if not (available['conversation'] and available['actions_outcomes']) and final!='unknown':errors.append('execution:final_comparison_withheld')
 return errors
