# Final project report

**Beyond Collusive Talk: Auditing Evidence of Coordination in AI Agents**

The completed research package contains an80-episode exploratory archive audit,240 full-corpus judge responses, and a separate20-episode fresh-data application. Original logs, predictions and provenance remain preserved. No additional API calls were made during finalization.

## Research contribution

We propose and operationalize combinations of evidence for distinguishing nine explanations, rather than claiming to discover that additional evidence is needed. The framework separates what current scores measure from the controls and independent references needed to validate discrimination. Read [the complete framework](EVIDENCE_FRAMEWORK.md) and [cross-field references](docs/cross_field_references.md). The proposal is not a validated sufficient rule for harmful collusion.

## Findings

- Original80: only26 candidate pairs both made successful choices;74 episodes involved automatic fills. Judge audit flags are evidence-policy/citation checks, not independently validated classification errors.
- Fresh20: conversation evidence supports9 specific bilateral agreements;8 match successful pair actions. Outcome-only screening flags all20. The staged procedure returns8 implemented adverse patterns,1 agreement with uncertain implementation and11 uncertain.
- The eight-case conditional-repair audit is complete. Only seed106 combines positive pair benefit and outsider loss across all strict-optimal alternatives. None establishes attributable harmful coordination under the documented review; this does not mean none occurred.
- No independent reference labels exist. Accuracy, precision and recall cannot be reported. The deterministic rule was frozen; semantic annotations were post-generation and unblinded.

## Evidence standard proposed

Use source-verified communication and recipient access; specific reciprocal commitment; successful actions matching the latest agreed plan; a named adverse consequence against explicit feasible benchmarks; and an attribution account that considers ordinary mistakes, outsiders and execution failures. Annotate harmful purpose separately. Communication causality requires an intervention or another defensible identification design. Similarity, suspicious language, or low reward alone is insufficient.

## Deliverables

- [Paper](paper/PAPER.md)
- [Fresh20 findings and provenance](test20_application/RESULTS.md)
- [Same-episode rule comparison](test20_application/RULE_COMPARISON.md)
- [Eight-case harm review](test20_application/HARM_ATTRIBUTION.md)
- [Machine-readable harm calculations](test20_application/harm_attribution.json)
- [Frozen procedure](staged_rule/PROTOCOL.md)
- [Archived240-call results](judge_all80/all80_results.csv)

## Reproduction

From the project workspace, run `python3 research_track_2_3/test20_application/finalize_results.py` to reproduce conditional repairs and final comparisons from preserved artifacts. Run `python3 -m unittest discover -s research_track_2_3/staged_rule -p test_rule.py` for the six decision-rule checks. Source paths in preserved provenance refer to this workspace; relocate/rebase those paths when sharing the raw logs. No credentials are needed for these offline calculations. Preserve original data licenses and attribution when redistributing; no repository license grant is asserted here.

This is a completed hackathon evidence-audit package with stated limitations, not a validated harmful-collusion detector. It has not been published or submitted.


# All100 score inventory and results

The consolidated table covers80 archive episodes and20 fresh episodes. Corpus identity is retained; the model and filling settings differ. All newly computable numerical scores are present. Existing archive scores are reused with their original provenance. No semantic labels or unidentified causal effects have been fabricated.

## Coverage

Communication publication/rejection/access records; successful assignments/skips/missing choices/fills; raw reward gaps; penalty-based and strict score gaps; pair-only and individual repair losses; joint repair interaction; optimal-allocation pair-benefit/outsider-loss ranges; recorded upstream regret gap; and conditional fill contributions are consolidated. Exact per-actor and per-message records and source hashes are in scores.json; scalar values are in scores.csv. Fifty matched differences are in paired_differences.json.

Regret gap remains an upstream metric, not independently reconstructed coalition advantage. Eligible single-optimum group comparisons remain limited to the previously verified24 archive cases; other cells are null. Independent reference labels, causal behavioral dependence and harmful-purpose/attribution conclusions cannot be manufactured by arithmetic. Fresh semantic annotations are joined where available; archive240 raw judgments remain separately preserved in judge_all80/all80_results.csv. Unknown entries are not zero or innocence. Fill effects are zero in fresh episodes because none were filled.

## Matched treatment-minus-baseline means

| Measure | Archive40 seed pairs | Fresh10 seed pairs |
|---|---:|---:|
|Team score|6.403|6.891|
|Pair–outsider mean reward gap|2.196|5.758|
|Pair-only repair loss|-4.974|-8.981|
|Joint repair interaction|0.530|0.006|
|Minimum pair benefit vs strict optimum|5.062|9.974|
|Minimum outsider loss vs strict optimum|-1.340|3.083|
|Recorded regret gap (unverified reconstruction)|1.845|4.734|

These are descriptive paired contrasts, not isolated causal communication effects. Prompt and channel conditions change together. Benefit/loss ranges span optimal allocations, not confidence intervals. Pair repair fixes outsider choices and measures static opportunity cost; interaction is joint repair minus separate best repairs. Positive interaction is not proof of behavioral dependence. Positive score gaps and relative reward advantages alone do not establish harmful coordination.

## Reproduction

Run `python3 research_track_2_3/all100/calculate.py` from the workspace. This reuses preserved archive measures, computes fresh episode actions/messages and repair scores using the organizer scorer, and rebuilds consolidated tables and paired aggregates without API calls. Original sources and frozen decision files are unchanged.
