"""Synthetic unit fixtures only; not experimental annotations."""
import copy,unittest
from score_reviews import compare

def fixture(who,values):
 return {'reviewer_id':who,'reviewer_type':'human','rubric_version':'0.1','status':'complete','cases':[{'case_id':str(i),'agreement':v,'execution':'unknown','harm':'unknown','dependence':'not_estimated','category':'uncertain','rationale':'Synthetic fixture','prior_exposure':'synthetic','evidence_events':[]} for i,v in enumerate(values)]}
class ScoringTests(unittest.TestCase):
 def test_known_agreement(self):
  a=fixture('A',['supported','not_supported']);b=fixture('B',['supported','not_supported'])
  self.assertEqual(compare(a,b)['dimensions']['agreement']['cohen_kappa'],1)
 def test_opposite(self):
  self.assertEqual(compare(fixture('A',['supported','not_supported']),fixture('B',['not_supported','supported']))['dimensions']['agreement']['cohen_kappa'],-1)
 def test_undefined_kappa(self):
  self.assertIsNone(compare(fixture('A',['unknown']),fixture('B',['unknown']))['dimensions']['agreement']['cohen_kappa'])
 def test_no_silent_drop(self):
  with self.assertRaises(ValueError):compare(fixture('A',['unknown']),fixture('B',['unknown','unknown']))
 def test_draft_rejected(self):
  a=fixture('A',['unknown']);a['status']='draft'
  with self.assertRaises(ValueError):compare(a,fixture('B',['unknown']))
if __name__=='__main__':unittest.main()
