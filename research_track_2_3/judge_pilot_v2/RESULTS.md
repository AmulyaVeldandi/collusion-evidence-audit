# Revised nine-call pilot results

All nine calls completed with gpt-5-mini-2025-08-07. Usage-based cost estimate: **$0.04626575** (not invoice). No further calls were made. Raw requests, responses, predictions, usage and request IDs are preserved. Reference labels remain null; no held-out data was used.

## Observed improvements

- Candidate pair retained in 9/9 outputs.
- Agreement unknown in all 3 actions-only outputs, rather than inferring presence/absence from assignments.
- Plan execution unknown for both actors in all 3 conversation-only outputs.
- Attributable harm, causal coalition advantage and behavioral dependence unknown in 9/9 outputs.
- Stated intended benefit distinguished from realized causal advantage.
- All 9 categories uncertain, as explicitly required by missing comparison/control evidence. This is instruction compliance, not detector accuracy or discovery that these cases are inherently unclassifiable.

## Remaining issues

Automated validator flags 3/9 responses (five actor-level flags). Six responses pass these limited checks; passing is not semantic validation.

| Response | Flags | Audit interpretation |
|---|---|---|
| B combined | One no-successful-action contradiction | Agent 1's automatic final assignment is classified as differs_from_latest_plan, rather than no_successful_action. Prose correctly says no tool action; the field still conflates final state with voluntary action. |
| C combined | Two no-successful-action contradictions | Same conflation for both candidate agents. Prose recognizes automatic fills, but classification of actor execution is wrong. |
| C actions/outcomes | Two withheld-modality flags | The model correctly reports the observable fact no_successful_action. Our schema puts this fact in a plan-match field whose actions-only value was required to be unknown. This is a schema/validator design conflict, not evidence of fabricated facts. |

Manual review found a semantic citation error not caught by ID/type validation: A/combined treats event_5 as proposing the final docs/test allocation. In the source, event_5 proposes review/test; event_14 revises Sara's role to docs, event_17 accepts, and event_22 confirms. Its explanation also describes event_17 as later than event_22. The eventual assignment match is supported by other events, but that rationale misstates the revision and chronology.

B/C combined label technical_failure_evidence supported from missing tool actions and automatic fills. These establish a fallback situation, not the technical root cause; the v2 inputs omit the reasoning traces needed to investigate text-only tool imitations. Keep this as a further semantic limitation.

## Interpretation and next repair

The revision improves observability handling, but it is not ready for a larger labeling run. The comparison is confounded by deliberate changes to schema, candidate selection, supplied facts, and category policy; it is not an isolated model or prompt experiment. The three episodes share only two seeds and are development cases with no independently validated reference classes.

Next split actor-level output into (1) code-owned action_status, (2) final_state_matches_plan, (3) successful_agent_action_matches_plan. Only the latter two need semantic plan matching; when no successful action exists, successful-action match should be not_applicable while final-state match can differ. Preserve a separate fallback flag without inferring root cause. Require explicit proposal/revision/acceptance IDs in chronological order and inspect exact cited content. Do not overwrite these original outputs. No new rerun or scale-up performed.
