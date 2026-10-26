# From adjacent literature to testable collusion evidence

Research question: which additional observations distinguish harmful coalition behavior from common incentives, unimplemented talk, and harm without established agreement? This is a proposed empirical adaptation, not a legal test or established new detector.

| Prior work / established observation | Proposed operationalization in our project | Availability and limitation |
|---|---|---|
| [Kovacic, Marshall, Marx & White (2011), Plus Factors and Agreement in Antitrust Law](https://repository.law.umich.edu/mlr/vol110/iss3/1/): organize evidence beyond parallel conduct by how strongly it favors coordinated over unilateral explanations. | Compare the coalition explanation with shared-task incentives, capability differences, turn order and environment fills. Require specific commitments and plan-linked conduct rather than similar actions alone. Treat several correlated clues as a bundle, not independent votes. | Application-level publication, access and action records exist. No verified independence controls. Our feature choices and combination rules are a proposed adaptation, not copied legal doctrine. |
| [Lowe et al. (2019), On the Pitfalls of Measuring Emergent Communication](https://arxiv.org/abs/1903.05168): messages can predict subsequent actions without affecting the environment or another agent. | Separate message/action consistency from behavioral dependence. Acknowledgment and agreement are observational signals; causal dependence needs controlled signal changes. | We can examine alignment with plans. Existing baseline/treatment arms do not isolate communication effects; prompts/channels and other behavior vary. Dependence remains unestimated. |
| [Jaques et al. (2019), Social Influence as Intrinsic Motivation](https://proceedings.mlr.press/v97/jaques19a.html): assess influence through counterfactual alternatives and their effects on other agents. | Specify the intervention and recipient action whose change would support influence. Never substitute a reward gap for that test. | This is a methodological reference, not a collusion detector. The fixed80 archived runs do not provide the required controlled alternatives; no new experiments are assumed. |
| [Nakamura et al. (2026), Colosseum, v2](https://arxiv.org/abs/2602.15198v2): compares communication and action-based collusion and already reports collusion on paper; action analysis uses regret relative to cooperative optimum. | Reuse the environment logs and distinguish proposed plans from successful implementation. Audit fallback assignments before interpreting outcomes. If implementing the paper's metric, reproduce its precise regret definition and feasible optimum. | Conversation/action disagreement is not our novelty. Our current raw mean reward gap is not the paper's regret-based advantage. A third-party fine-tuned-model dataset and its interface failures do not invalidate the original paper's results. |

Sources above were checked on 2026-10-24. Scope of this table: verified publication abstracts and previously inspected local experiment artifacts; not an exhaustive systematic literature review or a fresh full-text legal analysis. No claim that ML generally ignored antitrust is established by this table.

## Crucial adaptation

In this cooperative task, agreement is expected and can be legitimate. Antitrust's inference-of-agreement problem helps organize evidence, but agreement alone does not identify deviation from the team's objective. The project must separately establish implementation and attributable harm. Private access is opportunity for coordination, not proof of a harmful pact. A successful post is publication, not proof of recipient exposure or influence.

## Candidate rules to compare (not selected or frozen)

- Conversation rule: explicit reciprocal plan commitment by a prespecified pair. This detects agreement, not necessarily collusion.
- Outcome proxy: positive raw pair-versus-outsider mean reward gap. This is deliberately weak; differences in capabilities and costs can explain it. Do not rename it causal benefit.
- Agreement + implementation: reciprocal commitment plus actual pair assignment tools matching the latest plan. Record partial implementation by actor; exclude fills from agent conduct.
- Agreement + implementation + attributable harm: add a verified feasible comparator showing harm associated with the implemented coalition plan. Counterfactual optimization can support outcome assessment but does not automatically establish a causal communication effect.

Use three-valued logic: supported, not supported in adequate observed record, unknown. Missing harm evidence makes the last rule unassessable, not a validated negative. Keep each rule's target distinct: comparing accuracy against a harmful-collusion reference must expose false positives from agreement-only rules. Reference adjudication must not mechanically copy the rule under test.

## What the 15-run review currently permits

The source-linked review finds explicit pair or shared-team plan commitments in both arms. Pair actions match plans where successful actions exist, but several pairs have missing actions followed by environment fills. This supports a descriptive analysis of agreement/implementation and false inference hazards. It does not yet establish the three target classes or causal dependence.

Next research task: inspect available task costs, scoring code, and optimum artifacts for a reproducible feasible harm comparator in the reviewed runs. Preserve original data and assess whether those artifacts are trustworthy before calling any case harmful. Independently check provisional reviews if possible. If validated class coverage remains unavailable within the80 runs, report that limitation and restrict the claim to evidence sufficiency/observability rather than detection accuracy.
