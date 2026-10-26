import unittest
from rule import evaluate
class Rules(unittest.TestCase):
 def record(self):
  r={k:{'status':'unknown','evidence':[]} for k in ['Q','A','I','P','L','D','G','M','C']};r['candidate_execution']=[];return r
 def support(self,r,*keys):
  for k in keys:r[k]={'status':'supported','evidence':['source:event']}
 def implementation(self,r):
  self.support(r,'I');r['candidate_execution']=[{'actor':a,'action_status':'successful_assignment','matches_latest_plan':True,'action_evidence':['event']} for a in ['a','b']]
 def test_uncertainty_and_observability(self):
  r=self.record();self.assertEqual(evaluate(r,{})['verdict'],'insufficient_observability');self.support(r,'Q','A');self.assertEqual(evaluate(r,{})['verdict'],'agreement_implementation_unknown')
 def test_fills_cannot_implement(self):
  r=self.record();self.support(r,'Q','A');self.implementation(r);r['candidate_execution'][1]['action_status']='automatic_fill';x=evaluate(r,{});self.assertNotEqual(x['verdict'],'implemented_coordination_harm_unresolved');self.assertTrue(x['audit_flags'])
 def test_loss_does_not_prove_harm(self):
  r=self.record();self.support(r,'Q','A','L');self.implementation(r);self.assertEqual(evaluate(r,{})['verdict'],'implemented_coordination_adverse_pattern')
 def test_sabotage_without_pair_gain(self):
  r=self.record();self.support(r,'Q','A','L','M','P');self.implementation(r);r['M'].update(comparator_id='counterfactual_1',alternatives_considered=['allocation_error','fills']);self.assertEqual(evaluate(r,{})['verdict'],'supported_deliberately_harmful_coordination');self.assertEqual(r['G']['status'],'unknown')
 def test_no_action_vs_withheld(self):
  r=self.record();self.support(r,'Q','A');r['I']['status']='unsupported_in_adequate_record';r['complete_action_record']=True;self.assertEqual(evaluate(r,{})['verdict'],'agreement_without_full_pair_implementation');r['complete_action_record']=False;self.assertEqual(evaluate(r,{})['verdict'],'agreement_implementation_unknown')
 def test_intervals_need_fixed_thresholds(self):
  r=self.record();r['outcome_intervals']={'pair_benefit_min':1,'outsider_loss_min':2,'benchmark_id':'strict_optimum'};self.assertIsNone(evaluate(r,{})['robust_distributive_screen']);self.assertTrue(evaluate(r,{'pair_benefit_threshold':0,'outsider_loss_threshold':0})['robust_distributive_screen'])
if __name__=='__main__':unittest.main()
