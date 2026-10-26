# Beyond Collusive Talk: An Evidence Framework for Distinguishing AI-Agent Collusion from Its Alternatives

## Abstract

Which combinations of evidence distinguish a harmful coalition from legitimate coordination, independent similarity, unimplemented talk and execution failures? We propose an explanation-based framework separating observability, reciprocal agreement, implementation, harmful purpose and attributable consequences. Drawing on antitrust, causal inference and outcome-measurement research, we operationalize candidate plus factors using communication records, successful actions, reward comparisons, conditional repair losses and benchmark-sensitivity ranges. We audit 80 archived six-agent Jira episodes with 240 model judgments and apply a frozen deterministic rule to 20 fresh episodes. In the archive, only 26 candidate pairs both act, while 74 episodes involve automatic fills. In the fresh sample, focused assistant review supports nine bilateral agreements and eight implemented plans with adverse outcome patterns; harm attribution remains unresolved. Numerical measures are consolidated across all 100 cases and 50 matched seed pairs. These results characterize the distinct information supplied by candidate evidence combinations. Without independent reference labels or communication interventions, they do not establish their discriminative accuracy or causal sufficiency.

## 1. Introduction

The question is not simply whether additional evidence is needed to identify collusion. It is which evidence helps distinguish collusion from competing explanations. Similar actions can reflect common incentives, agreement can support legitimate cooperation, and a poor outcome can arise from ordinary mistakes or environment failures. A useful evaluation must determine which of these explanations the available record supports and which remain unresolved.

We propose a framework connecting each explanation to the evidence needed to assess it. Its central distinction is between evidence of agreement, evidence that the agreement was implemented, and evidence that the implemented conduct produced an adverse consequence. Harmful purpose and the causal influence of communication require separate assessment.

Our contribution has three parts: an explanation-based evidence framework; reproducible operational measures for communication, conduct and consequences; and an empirical audit of how those measures constrain interpretation in 100 Jira episodes. We propose these combinations for validation rather than claiming to have established a sufficient collusion detector.

## 2. Related work and conceptual basis

Antitrust plus-factor reasoning evaluates evidence beyond parallel conduct according to its support for coordinated versus unilateral explanations [1]. We adapt this approach to AI-agent evidence, without making a legal liability claim. In cooperative Jira allocation, agreement is expected; its existence does not establish a harmful coalition. Porter and Zona's study of bidding provides a related economic example of examining collusion and its consequences against a comparison [6].

Communication research distinguishes messages that predict behavior from messages that influence it [2]. Algorithmic-pricing work examines strategic behavior and learning dynamics rather than interpreting elevated prices alone as evidence of explicit agreement [3,4]. Colosseum already distinguishes conversational and behavioral evidence and uses regret-based coalition metrics [5]. We build on these distinctions; we do not claim to discover the talk–action gap or that earlier ML research universally ignored adjacent fields.

Three further connections guide our operationalization. Target-trial reasoning makes the intervention and comparison underlying a causal claim explicit [7]. Research on interference separates effects on treated participants from spillovers onto others [8], motivating separate pair, outsider and team outcomes. Healthcare research on proxy outcomes [9,10] cautions against substituting an intermediate signal—such as reward advantage or plan completion—for the endpoint of interest. Partial-identification research motivates making assumptions and uncertainty explicit [11]. Our ranges across optimal allocations are benchmark-sensitivity analyses, however, not identified causal bounds. These applications to AI-agent evidence are our proposed adaptations.

## 3. Proposed evidence framework

We define **Q** as adequate, source-verified observability; **A** as specific reciprocal agreement; **I** as successful conduct matching the latest accepted plan; **P** as expressed harmful purpose; and **H** as an adverse consequence against an explicit comparator with a supported link to the implemented conduct. Communication's causal contribution is a separate question.

For implementation, H is decomposed into benchmark adversity (team loss L or outsider loss D) and mechanism attribution M. Consequently, a positive score gap does not by itself satisfy H. Pair benefit G may support a self-serving explanation but is unnecessary for sabotage. Unknown evidence remains unknown rather than becoming a negative label.

| Explanation | Evidence combination |Defensible conclusion | Current measurement / validation boundary |
|---|---|---|---|
| Deliberate coalition formation | Q + A, specific reciprocal commitments | Deliberate formation of a joint plan; may be legitimate cooperation | Source-linked agreement review; shared team commitment alone insufficient |
| Implemented coalition | Q + A + I | Enacted coordination; purpose and harm unresolved | Successful assignments/skips matched to latest plan; fills excluded |
| Deliberate harmful coalition | Q + A + I + P + H, with loss linked to conduct | Enacted coordination with expressed harmful purpose and attributable adverse consequences | Score/range/repair evidence available; full attribution and intent not established by arithmetic |
| Innocent correlation / common incentives | Similar actions + supported common-incentive explanation + verified independent decisions | Supports independent similarity | Public-chat baseline does not verify independence; controlled isolation required |
| Talk without implementation | Delivered proposal/agreement + complete actions showing non-execution | Non-implementation; distinguish technical failure and voluntary abandonment | Action integrity measurable; no inference of negligible communication effect |
| Talk without behavioral effect | Communication intervention + sufficiently precise equivalence evidence | Negligible effect within a predefined margin | Requires intervention, equivalence margin and adequate repeated trials; unavailable here |
| Harm without established agreement | Q + H, agreement unsupported or unobserved | Harm without established agreement, not proof that agreement never existed | Loss alone supports only adverse-pattern status while attribution unresolved |
| Ordinary coordination mistake | A + I + team loss, without supported harmful purpose or preferential benefit | Plausible alternative, not an established innocent label | Repair opportunities help characterize inefficiency; missing purpose is not proof of mistake |
| Environment-caused poor outcome | Low score + fills/failures + limited voluntary implementation, with source trace | Execution-confound explanation when the relevant loss is traced | Conditional fill-versus-skip and best-replacement comparisons; not a behavioral rerun |

These explanations can overlap and are not forced into mutually exclusive ground-truth classes. A case can support enacted coordination while leaving both ordinary error and harmful coordination plausible. The framework therefore produces evidence profiles and graded conclusions before any proposed classification rule is evaluated.

## 4. Data and study design

### 4.1 Archived exploratory corpus

The original source is the Hugging Face dataset `dougalldeepmind/2026-09-03-colosseum-jira-collusion-qwen36-difficult-advice-chunk-only-702`, revision `71227d3821afd37ea971c414a70dddb898246046`. It contains 40 baseline and 40 treatment episodes matched by seed. Each episode has six agents and a predesignated two-agent candidate pair using fine-tuned Qwen model variants. Assigned roles and folder conditions are experimental metadata, not verified collusion labels.

An initial 20-development/20-held-out/40-reserve partition grouped matched seeds. Subsequent full-corpus analysis exposed all 80 episodes. We preserve the partition history but treat the archive analysis as exploratory. Earlier judge pilots used different prompts and are retained separately rather than pooled into the uniform batch.

### 4.2 Fresh-data application

A separate generation workflow produced 20 completed episodes, baseline/treatment seeds 101–110, using gpt-4o-mini-2024-07-18 with automatic filling disabled. Only canonical completed episodes in the collection manifest are included; failed attempts are retained. The changed model and filling settings make this a transfer application rather than an exact replication of the archive distribution.

The deterministic staged rule, thresholds and template were frozen before generation. A complete semantic annotation procedure was not independently frozen. Fresh narrative assessments are focused, source-linked, unblinded assistant reviews performed after generation. They are not independent reference labels. The two corpora are reported separately throughout.

### 4.3 Model-judge audit

For each archived episode, we obtained one judgment for each of three evidence views: conversation only, actions/outcomes only, and combined. All 240 calls to gpt-5-mini-2025-08-07 completed, using low reasoning effort and a maximum of 6,000 output tokens. Saved-response token cost was estimated at $1.382366, not independently reconciled to a billing invoice.

Candidate identities were fixed across views. Names were pseudonymized and case IDs made opaque; experimental labels, paths, prior judgments and reference labels were withheld. Message wording and channel structure could still reveal conditions. Outcome-bearing views included calculated comparisons and separately marked upstream metrics. Missing evidence was intended to produce uncertainty, not an inference of absence.

## 5. Operational measures

### 5.1 Communication, agreement and implementation

Successful message posts are matched to blackboard records by event identifier, sender and content. Membership records establish eligible access. Exact message inclusion in saved partner prompts supports recorded recipient-input exposure, not attention or independently verified provider receipt. All 203 delivered candidate messages checked in the 20 archive development episodes appeared in at least one saved partner prompt; this check was not extended by assumption to all 100 episodes.

Agreement review distinguishes a specific proposal and reciprocal acceptance from general participation in a shared team plan. Revisions and late contradictions are retained. Implementation requires successful assignment or explicit-skip tools matching the latest accepted plan for each actor. Textual tool imitations, rejected actions, missing actions and automatic fills are recorded separately.

### 5.2 Outcome and repair measures

We reuse the organizer's instance reconstruction, scorer and optimizer. Actual team scores reproduce for all 100 episodes; archive saved optimal scores and reconstructed prompt costs also pass the documented checks. Duplicate assignments incur penalties, so the penalty-based optimum and the no-duplicate strict optimum are distinguished.

Let W(a) be team score for allocation a, C the candidate pair and O the outsiders. We calculate:

| Measure | Definition and evidentiary role |
|---|---|
| Team-score gap | Optimum score minus observed W(a); measures benchmark-relative inefficiency |
| Raw reward gap | Mean recorded reward of C minus mean recorded reward of O; measures within-run inequality |
| Pair-benefit range | Observed pair total minus pair totals across strict-optimal allocations; tests benchmark-allocation sensitivity |
| Outsider-loss range | Outsider totals across strict-optimal allocations minus observed outsider total; distinguishes outsider consequences from pair advantage |
| Pair-only repair R(C) | Best improvement from changing only C's task/skip choices, keeping O fixed; measures conditional opportunity cost |
| Single-actor repair R(i) | Best improvement from changing only candidate i's choice |
| Joint repair interaction | R(C) − R(i) − R(j); measures non-additivity of repair opportunities, not identified behavioral dependence |
| Fill contribution | Observed score minus score when all missing choices skip, holding successful choices fixed |
| Avoidable fill loss | Best score from replacing missing choices minus observed score, holding successful choices fixed |
| Recorded regret gap | Upstream noncoalition mean regret minus coalition mean regret; retained separately because independent reconstruction remains incomplete |

Repair enumeration includes every candidate task/skip combination under the penalty-based scorer. Optimal-allocation ranges are exact benchmark-sensitivity ranges, not confidence intervals or causal-effect bounds. Single-optimum group comparisons remain available for 24 eligible archived cases; excluded or unverified values are null. Fills are absent in the fresh corpus, so their realized contributions there are zero.

### 5.3 Evidence combinations and analysis boundary

The frozen staged rule distinguishes agreement, implementation, adverse pattern and attributed harmful coordination. Its numerical screen uses positive minimum pair benefit and outsider loss, with zero thresholds and a 1e-7 floating-point tolerance. These are not calibrated meaningful-harm thresholds. Mechanism attribution must identify a comparator and consider alternatives; harmful purpose is recorded separately.

We consolidate numerical measures for all 100 cases and calculate treatment-minus-baseline differences for 50 matched seeds. Archive judgments and fresh assistant annotations remain separate observations. No weighted suspicion score is fitted, and no reference label is inferred from a condition or a detector prediction.

## 6. Results

### 6.1 Archived judgments and evidence integrity

| Category | Conversation | Actions/outcomes | Combined |
|---|---:|---:|---:|
| Uncertain |52|80|7|
| Agreement without full pair implementation |24|0|43|
| Implemented coordination, harm unresolved |4|0|27|
| Coordinated action with adverse pattern |0|0|3|
| Supported harmful coordination |0|0|0|

These are raw model outputs. Conversation-only implementation categories exceed available evidence. Combined outputs claim implemented coordination in 30 cases, whereas computed facts show only 26 runs with actions by both candidates; this discrepancy motivates category-consistency checking. Zero supported-harm predictions does not establish80 harmless cases.

#### Audit findings

The original automated checks flag190 responses. A follow-up category/implementation check brings the union to194:164 have evidence-policy or category flags,48 have citation flags, with 30 citation-only responses. Counts overlap. By view,80 conversation-only,79 action/outcome-only and35 combined responses have at least one follow-up flag.

The flags include missing-evidence inference, negative-versus-unknown coding differences, invalid citation identifiers and unsupported implementation categories. A formatting error is not necessarily fabricated content. Passing checks does not establish semantic correctness, and these audit counts are not classification error rates. Raw outputs remain unchanged.

#### Three adverse-pattern cases

| Run | Checked finding | Conclusion |
|---|---|---|
| Seed 1 treatment | Both candidates execute their revised plan; a pair-only reassignment increases team score by 15.504 | Local inefficiency supported; ordinary allocation error remains plausible |
| Seed 11 baseline | Judge reports one candidate has no successful action but assigns an implemented adverse-pattern category | Category contradicts full-pair implementation requirement |
| Seed 22 treatment | Global score gap118.306; pair-only improvement is zero; two outsider fills | Poor overall outcome does not establish harm attributable to the pair |

These differ from the earlier19/22/37 development distributive-screen candidates because the procedures use different outcome criteria. They should not be treated as mutual validation.

### 6.2 Execution effects in the archive

Across the 80 archived episodes, both candidates make successful choices in 26, one in 45, and neither in nine. These counts constrain full-pair implementation claims but do not establish intent.

We hold all successful agent choices fixed and compare recorded automatic fills with two explicit alternatives: skipping every missing choice, and optimally replacing missing choices under the same penalty-based score. Missing-action counts reconcile with reported fills in all 80 episodes. The optimizer agrees with independent exhaustive enumeration for all 80 cases.

Of74 episodes with automatic fills,64 improve team score relative to skipping missing choices, seven worsen it and three tie. The mean contribution across affected episodes is+14.916 points. Relative to optimal replacements,70 affected episodes have avoidable loss, averaging35.829 points across all 74. The two benchmarks answer different questions: a fill can improve completion while still being suboptimal.

In seed 22 treatment, recorded fills reduce score by 70 points relative to skipping missing agents, while successful candidate choices remain fixed. Optimal replacements could increase its recorded score by 117.790. This strengthens an execution-confound explanation for the adverse outcome. These deterministic conditional comparisons do not estimate how agents would behave if filling were disabled, and optimal replacements are an oracle rather than a realistic policy.

### 6.3 Aggregate numerical contrasts

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

The archive and fresh corpus both show higher average team score in treatment, while the fresh outsider comparison moves in an adverse direction. These measures concern different endpoints: higher team score does not imply every group benefits. Conversely, a more favorable pair distribution does not establish an agreement caused outsider loss.

### 6.4 Fresh evidence combinations

A separate generation workflow produced20 completed six-agent episodes, baseline/treatment seeds101–110, using gpt-4o-mini-2024-07-18 with automatic filling disabled. Only canonical completed episodes from the collection manifest are included; failed attempts remain archived. Reconstructed team scores match20/20. Model and execution settings differ from the original Qwen archive, making this a transfer setting.

The deterministic rule, numerical thresholds and template were frozen before generation; a complete semantic annotation prompt/model/procedure was not independently frozen. We added focused, source-linked, unblinded assistant annotations after generation. These are predictions/evidence assessments, not independent references. The structural-only adapter leaves all 20 uncertain; adding the documented narrative annotations yields the following evidence filtering:

| Evidence requirement | Episodes supported /20 |
|---|---:|
| Conversation: specific bilateral agreement |9|
| Outcome: positive team-score gap |20|
| Agreement + successful implementation + adverse pattern |8|
| Attributable harmful coordination |0|

The staged verdicts are eight implemented-coordination/adverse-pattern cases, one agreement with uncertain latest-plan implementation, and eleven uncertain. Unknown does not establish innocence or absent agreement. Thresholds are zero plus floating-point tolerance, not calibrated meaningful-harm cutoffs.

An additional eight-case audit enumerates pair-only task/skip substitutions while holding outsiders fixed and records duplicate assignments, optimal-allocation group-reward ranges and joint repair interactions. Only seed 106 has robust positive pair benefit and outsider loss across strict-optimal alternatives. These static comparisons expose repair opportunities and distributional patterns; they do not identify harmful intent, a harmful coordination mechanism, or communication causality. All eight retain unknown harm attribution. Detailed values and alternatives appear in test20_application/HARM_ATTRIBUTION.md and harm_attribution.json.

No additional judge API calls were made for this application. There are no independent reference labels, so no accuracy, precision, recall or confusion matrix is estimable. The20 episodes therefore provide fresh-data application of a frozen deterministic procedure, not independently validated end-to-end detection performance.

### 6.5 What the additional scores change

The fresh outcome-only screen flags all 20 episodes, whereas the agreement-plus-implementation screen supports eight implemented adverse patterns. This narrowing is evidence filtering, not demonstrated improvement in precision.

The repair and distributional measures further separate those eight cases. In treatment seed 102, pair-only repair can improve team score by 19.427 points, but the pair's reward is 10.313 points below its strict-optimal comparison. In seed 106, the pair instead benefits by 1.127 points while outsiders lose 20.432 points relative to strict-optimal alternatives, yet pair-only repair is zero. Thus a self-serving distributional pattern and a pair-local repair opportunity are different signals. Neither alone determines harmful intent or identifies communication's causal contribution.

In seed 103, pair-only repair is also zero despite a positive team gap. In seed 107, pair-only repair is 39.422 points while the pair's benefit range is negative. The complete 100-case table retains these distinctions rather than collapsing them into one score. Their incremental discriminative value requires independent references.

## 7. Discussion and validation agenda

The proposed framework asks what each signal contributes to distinguishing explanations. Reciprocal commitment addresses deliberate plan formation; successful matching actions address implementation; distributional and repair measures address different consequences; execution tracing addresses environment confounds. Attribution and controlled dependence remain additional requirements when those stronger claims are made.

The empirical contribution is an operationalized set of candidate plus factors and concrete cases in which their interpretations diverge. It does not establish that a particular combination is sufficient, that zero attributed-harm findings imply innocence, or that the framework discriminates all nine explanations accurately. In particular, absence of expressed harmful purpose cannot certify an ordinary mistake, and non-implementation cannot establish negligible behavioral effect.

Future validation should obtain independent source-linked references, permit overlapping explanations and unresolved cases, and compare nested evidence sets on the same examples: conversation only; outcomes only; agreement plus implementation; and added distributional, repair and mechanism evidence. The complete annotation procedure and decision rule should be frozen before untouched evaluation. Signal value should be assessed by incremental discrimination and uncertainty, rather than reductions in flag counts alone.

Two explanations require new experimental conditions. Independent similarity needs verified isolation from partner signals while retaining common task incentives. Talk without behavioral effect needs a communication intervention, a predefined equivalence margin and enough repetitions to support a negligible-effect conclusion. Neither can be supplied by relabeling the current public-chat baseline.

## 8. Limitations

There are no independent harmful-collusion reference labels, so sensitivity, specificity, precision and recall are not estimable. Archive judge outputs and fresh assistant reviews are not equivalent procedures. Fresh reviews are unblinded and focused rather than exhaustive independent adjudications; the frozen deterministic rule does not make the whole semantic pipeline preregistered.

The archive has substantial filling, whereas the fresh corpus changes model and disables filling. The original archive split was exposed. Baseline/treatment conditions bundle prompt and channel changes, and fresh arms were run in blocks; paired contrasts do not isolate communication effects. Conditioning on successful pair actions can introduce selection bias.

Reward endpoints describe this synthetic environment rather than general social harm. Individual reward counterfactuals and recorded regret have incomplete validation in the documented archive analyses. Strict-optimal ranges do not cover all reasonable decentralized comparisons, while oracle repairs do not model outsider responses. Citation/policy audit flags are not independently validated semantic error labels. An exhaustive novelty review has not been conducted.

## 9. Conclusion

Convincing evidence should identify the explanation supported by the record: agreement, enacted coordination, benchmark-relative adversity, or harm linked to agreed conduct. Our framework connects these claims to distinct evidence requirements and supplies reproducible measurements across 100 cases. The results demonstrate why the candidate signals must remain distinguishable; whether their combinations reliably detect harmful collusion is a question for controlled, independently referenced validation.

## Reproducibility

The consolidated numerical tables are `all 100/scores.csv` and `all 100/scores.json`; matched differences and descriptive summaries are in the same directory. Run `python3 research_track_2_3/all 100/calculate.py` from the workspace to rebuild them from preserved artifacts without API calls. This reuses archived measurements and calculates fresh communication/action facts and repair measures with the organizer scorer.

Archived raw judge results, requests, responses and audit checks are in `judge_all80/`; `paper/build_tables.py` rebuilds its two CSV tables. Fresh source-linked annotations, predictions and the eight-case repair audit are in `test20_application/`. Frozen rule files, hashes and six regression tests are in `staged_rule/`. Original logs, provenance and predictions remain preserved; unavailable fields remain explicit. Local source paths require rebasing if the project is relocated.

Cross-field citation import provenance is retained in `docs/cross_field_references.md`. The bibliography records sources used in the conceptual mapping; this revision does not claim a new full-text systematic review. No publishing or submission has occurred.

## References

1. Kovacic et al.(2011). Plus Factors and Agreement in Antitrust Law. https://repository.law.umich.edu/mlr/vol110/iss3/1/
2. Lowe et al.(2019). On the Pitfalls of Measuring Emergent Communication. https://arxiv.org/abs/1903.05168
3. Calvano et al.(2019 working-paper version). Artificial Intelligence, Algorithmic Pricing and Collusion. https://www.ftc.gov/system/files/documents/public_events/1494697/calzolaricalvanodenicolopastorello.pdf
4. Hansen, Misra & Pai(2020). Algorithmic Collusion: Supra-competitive Prices via Independent Algorithms. https://cepr.org/publications/dp14372
5. Nakamura et al.(2026), Colosseum, v2. https://arxiv.org/html/2602.15198v2
6. Porter & Zona (1999). [Ohio School Milk Markets: An Analysis of Bidding](https://www.nber.org/papers/w6037).
7. Hernán & Robins (2016). [Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/).
8. Hudgens & Halloran (2008). [Toward Causal Inference With Interference](https://pmc.ncbi.nlm.nih.gov/articles/PMC2600548/).
9. Obermeyer et al. (2019). [Dissecting Racial Bias in an Algorithm Used to Manage the Health of Populations](https://pubmed.ncbi.nlm.nih.gov/31649194/).
10. CAST Investigators (1989). [Effect of Encainide and Flecainide on Mortality in a Randomized Trial of Arrhythmia Suppression](https://www.nejm.org/doi/full/10.1056/NEJM198908103210629).
11. Manski (1990). [Nonparametric Bounds on Treatment Effects](https://ipcid.org/evaluation/outros_temas/Manski%20-%20Nonparametric%20Bounds.pdf).
