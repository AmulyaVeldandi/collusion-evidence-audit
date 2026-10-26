import unittest,json
from pathlib import Path
from validate import validate
P=Path(__file__).resolve().parent
class Execution(unittest.TestCase):
 def make(self,view):
  e=json.loads((P/('case_C__'+view+'.json')).read_text());p={k:{'status':'unknown','evidence_ids':[],'explanation':''} for k in ['acknowledgment','reciprocal_agreement','stated_intended_benefit','attributable_harm','causal_coalition_advantage','behavioral_dependence','technical_failure_evidence']};p.update(candidate_members=e['candidate_members'],category='uncertain',execution_comparison_by_actor=[{'actor':a,'successful_action_matches_plan':'unknown' if view=='conversation' else 'not_applicable_no_successful_action','final_state_matches_plan':'differs' if view=='combined' else 'unknown','evidence_ids':[],'explanation':''} for a in e['candidate_members']]);return e,p
 def test_automatic_fill_can_differ_without_agent_deviation(self):
  e,p=self.make('combined');self.assertEqual(validate(p,e),[])
  p['execution_comparison_by_actor'][0]['successful_action_matches_plan']='differs';self.assertIn('execution:no_agent_action',validate(p,e))
 def test_actions_only_no_action_is_observable(self):
  e,p=self.make('actions_outcomes');self.assertEqual(validate(p,e),[])
  p['execution_comparison_by_actor'][0]['final_state_matches_plan']='differs';self.assertIn('execution:final_comparison_withheld',validate(p,e))
 def test_conversation_does_not_establish_missing_action(self):
  e,p=self.make('conversation');self.assertEqual(validate(p,e),[])
  p['execution_comparison_by_actor'][0]['successful_action_matches_plan']='not_applicable_no_successful_action';self.assertIn('execution:actions_withheld',validate(p,e))
if __name__=='__main__':unittest.main()
