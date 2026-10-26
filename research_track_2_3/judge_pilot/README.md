# Nine-call judge pilot — completed after billing retry

Latest status: all nine calls completed after the user authorized a retry. Estimated token cost $0.032903. See RESULTS.md for substantive audit failures; these are not validated labels.

Initial attempt, 2026-10-24: prepared nine frozen requests; attempted case_A/conversation once. OpenAI returned HTTP 429, code `credit_balance_exhausted`. Zero model predictions were produced; eight requests were not sent. No automatic retries. Error and attempt metadata are preserved beside the requests.

Run `python3 research_track_2_3/judge_pilot/run.py` to reproduce/verify preparation without inference. `--run` sends requests, but deliberately refuses to repeat an unresolved attempt. After funding, archive the rejected attempt and error together before an explicitly requested retry; never delete failure history. Completed response files are skipped.

## Design

Three existing development cases, each with conversation-only, actions/outcomes-only, and combined evidence. These are three episodes from only two task seeds, not three independent tasks or validated examples of three target classes. Held-out cases were not read. No ground-truth labels or decision rules were changed.

Model: gpt-5-mini-2025-08-07, low reasoning, maximum 6,000 output tokens per call. Fixed snapshot chosen for a small reproducible process check, not a claim of optimal judge quality. Official documentation currently marks it deprecated; access was not verified because billing blocked generation. No automatic model substitution.

Pricing checked at https://developers.openai.com/api/docs/models/gpt-5-mini : $0.25 / million input tokens, $2 / million output tokens. A conservative UTF-8-byte input budget plus overhead and maximum outputs gives total $0.1584; runner refuses preparation above $0.50. This is a planning bound at those rates, not an actual bill or tokenization measurement.

Names are pseudonymized using existing mappings. Conditions, assigned coalition labels, upstream judge results, prior assistant reviews, and model reasoning traces are withheld. Conversation content may reveal treatment. Only posts matched to delivered board events appear; actual action tools and environment outcomes appear in behavioral views. Claims inside conversations remain claims. Automatic fills are explicitly distinguished from agent action. Rejected message attempts are omitted from the conversation view. These choices limit study of attempted-but-undelivered communication.

Each independent request has no shared conversation state or tools. All dimensions use the same schema; unknown is permitted. Candidate members are inferred by the judge, so membership may differ between views. Raw configured-pair reward gaps are not supplied: this pilot tests evidence interpretation, not a fixed-pair reward-gap detector. Full task costs, feasible harm counterfactuals, and causal interventions are unavailable. Benefit and dependence therefore cannot be assumed established.

Predictions, if produced, go in separate prediction files with reference_label=null, raw responses, usage, model, request identifiers and timestamps. Manifest records request/source hashes. Structured output validates shape, not scientific correctness. Event citation validity and substantive claims still require review. No accuracy, independent validation, category coverage, or causal conclusions can be reported from this failed pilot.
