# Execution correction v0.3 — prepared offline

Original v1/v2 inputs, predictions and flags are preserved. Nine evidence views copied byte-for-byte from v2; hashes verified. No API calls or new labels.

Code-owned observations record successful agent action status and final assignment origin. Judge output now has two independent comparisons: successful_action_matches_plan and final_state_matches_plan. A missing successful action requires not_applicable_no_successful_action when actions are observed; this is distinct from unknown when actions are withheld. An automatic final assignment may differ from the plan without constituting an agent deviation. Conversation plus outcome data are required for final-state matching.

Fallback evidence alone no longer warrants a technical root-cause claim. Instructions require proposal/revision chronology. Validators flag structural consistency errors but cannot prove semantic citation correctness.

Build: python3 research_track_2_3/judge_pilot_v3/build.py
Tests: python3 -m unittest discover -s research_track_2_3/judge_pilot_v3 -p 'test_*.py'

Three regression tests passed: missing action with different final state; observable absence of action without conversations; unknown execution when actions are withheld. This correction has not been tested with new live judge calls. Other v2 restrictions, including uncertainty forced by missing causal/harm evidence, remain; this is a consistency pilot rather than a validated classifier.
