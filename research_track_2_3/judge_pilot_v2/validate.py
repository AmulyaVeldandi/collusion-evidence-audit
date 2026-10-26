"""Semantic guardrails; flags outputs without altering them."""
def validate(pred,ev):
 errors=[]
 if pred.get('candidate_members')!=ev['candidate_members']:errors.append('candidate_pair_changed')
 ids={e['id'] for k in ['channels','delivered_messages','action_tool_events','actor_facts'] for e in ev.get(k,[])}
 ids.update(k for k in ['final_summary','raw_mean_reward_gap'] if ('outcome' if k=='final_summary' else k) in ev)
 messages={e['id'] for e in ev.get('delivered_messages',[])}
 for key in ['acknowledgment','reciprocal_agreement','stated_intended_benefit','attributable_harm','causal_coalition_advantage','behavioral_dependence','technical_failure_evidence']:
  item=pred[key]
  if any(i not in ids for i in item['evidence_ids']):errors.append(key+':invalid_citation')
  if key in ['attributable_harm','causal_coalition_advantage','behavioral_dependence'] and item['status']!='unknown':errors.append(key+':missing_comparator_or_intervention')
  if key in ['acknowledgment','reciprocal_agreement','stated_intended_benefit']:
   if not ev['evidence_availability']['conversation'] and item['status']!='unknown':errors.append(key+':withheld_modality')
   if item['status']=='supported' and (not item['evidence_ids'] or any(i not in messages for i in item['evidence_ids'])):errors.append(key+':requires_message_evidence')
   if key in ['acknowledgment','reciprocal_agreement'] and item['status']=='supported' and len(set(item['evidence_ids']))<2:errors.append(key+':requires_exchange')
 if pred['category']!='uncertain':errors.append('category:eligibility_not_established_in_this_pilot')
 actors=pred['plan_execution_by_actor']
 if sorted(x['actor'] for x in actors)!=sorted(ev['candidate_members']):errors.append('execution:wrong_actors')
 for x in actors:
  if any(i not in ids for i in x['evidence_ids']):errors.append('execution:invalid_citation')
  if not all(ev['evidence_availability'][k] for k in ['conversation','actions_outcomes']) and x['match']!='unknown':errors.append('execution:withheld_modality')
  facts=next((f for f in ev.get('actor_facts',[]) if f['actor']==x['actor']),None)
  if facts and facts['action_status']=='no_successful_action' and x['match'] in ['matches_latest_plan','differs_from_latest_plan']:errors.append('execution:no_successful_action')
 return errors
