# Evidence pilot v0.2 — pilot completed

This revision addresses the first pilot's specification defects. After explicit user authorization, nine API calls completed. See RESULTS.md; estimated token cost $0.04626575. Original v1 artifacts remain unchanged. Only case A/B/C development inputs were used; no held-out reads.

Build: `python3 research_track_2_3/judge_pilot/audit_communication.py` then `python3 research_track_2_3/judge_pilot_v2/build.py`.
Test: `python3 -m unittest discover -s research_track_2_3/judge_pilot_v2 -p 'test_*.py'`.

The nine JSON evidence views are paired with instructions.txt and schema.json. manifest.json records hashes. These are offline inputs, not API request/response artifacts. validate.py flags semantic violations without overwriting predictions; an eventual API runner should also validate JSON-schema shape.

## Changes

- Fixed candidate pair across views: A/B Agent 1 + Agent 5 (Jeanene/Sara), C Agent 1 + Agent 6 (Afton/Sheri). Selected from configured roles as a prespecified analysis subset, never a reference label. This changes the v1 free-selection task, so any later comparison is a pipeline revision comparison, not solely a prompt effect. Treatment metadata stays outside judge inputs.
- Publication verified mechanically against event ID, sender and content. Rejected attempts retained as facts, their message content omitted from delivered messages. Access permission does not establish recipient model-input exposure; exposure remains unknown.
- Successful assignment tools identified per actor. Final fills inferred only when the missing-action count reconciles with reported fallback count and assignment filling is enabled. This inference assumes complete action logs; it is labeled as such. A candidate successes:2; B:1; C:0. No intentional non-action or technical root cause inferred.
- Raw mean reward gap is computed for the fixed pair in outcome-bearing views, explicitly descriptive. It is not regret-gap advantage or causal improvement.
- Judge assesses specific acknowledgment, mutual agreement, latest-plan matching by actor, intended benefit and alternatives. Missing modalities require unknown. Harm/causal advantage/dependence require absent comparison/control data and are therefore unknown in this pilot.
- Target-category eligibility cannot be established with these limited inputs, so uncertain is required. This pilot tests evidence extraction and consistency, not discrimination among validated target categories. Do not present forced abstention as detector accuracy.
- Tests cover view separation, immutable evidence hashes, fixed membership, observed candidate execution counts, and deliberately invalid agreement/dependence/member predictions. Citation checks are necessary but do not guarantee semantic support. Tests passed (3).

## Next

Inspect the v2 inputs and definitions, then authorize a separate nine-call rerun if desired. Do not scale to 15 cases until field-level audit is acceptable and missing class coverage/comparator evidence is addressed. A new runner should preserve raw outputs and validation failures, compare per-field defects against v1, and keep references null. Full source task-cost tables and controls are still required for stronger conclusions.
