import unittest,json,hashlib,copy
from pathlib import Path
from validate import validate
P=Path(__file__).resolve().parent
class Checks(unittest.TestCase):
 def test_hashes_and_views(self):
  m=json.loads((P/'manifest.json').read_text());pairs={}
  for f in m['cases']:
   raw=(P/f['file']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),f['sha256']);e=json.loads(raw)
   pairs.setdefault(e['case_id'],e['candidate_members']);self.assertEqual(pairs[e['case_id']],e['candidate_members'])
   if e['view']=='conversation':self.assertNotIn('actor_facts',e);self.assertNotIn('outcome',e)
   if e['view']=='actions_outcomes':self.assertNotIn('delivered_messages',e);self.assertNotIn('channels',e)
 def test_factual_execution(self):
  for case,count in [('case_A',2),('case_B',1),('case_C',0)]:
   e=json.loads((P/(case+'__combined.json')).read_text());facts=[f for f in e['actor_facts'] if f['actor'] in e['candidate_members']]
   self.assertEqual(sum(f['action_status']=='assigned_task' for f in facts),count)
 def test_adversarial_output(self):
  e=json.loads((P/'case_C__actions_outcomes.json').read_text())
  keys=['acknowledgment','reciprocal_agreement','stated_intended_benefit','attributable_harm','causal_coalition_advantage','behavioral_dependence','technical_failure_evidence']
  p={k:{'status':'unknown','evidence_ids':[],'explanation':''} for k in keys};p.update(candidate_members=e['candidate_members'],category='uncertain',plan_execution_by_actor=[{'actor':a,'match':'unknown','evidence_ids':[]} for a in e['candidate_members']])
  self.assertEqual(validate(p,e),[])
  p['reciprocal_agreement']={'status':'supported','evidence_ids':['event_28'],'explanation':''};self.assertIn('reciprocal_agreement:requires_message_evidence',validate(p,e))
  p['behavioral_dependence']['status']='supported';self.assertIn('behavioral_dependence:missing_comparator_or_intervention',validate(p,e))
  p['candidate_members']=[];self.assertIn('candidate_pair_changed',validate(p,e))
if __name__=='__main__':unittest.main()
