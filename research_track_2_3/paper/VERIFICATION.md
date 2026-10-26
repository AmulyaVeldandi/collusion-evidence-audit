# Paper revision and numerical verification

The current draft integrates the new findings in Section6.5 and reports the principal results in the abstract. Tables1–7 have numbered captions; methods, findings, interpretation and limitations are kept distinct.

Verification completed:

- Included100-case scores and50 paired records, plus frozen-rule hashes: checked.
- Post hoc identity for both interval endpoints: maximum residual2.842170943040401e-14.
- Raw-positive / non-robust counts:25/33 archive,9/10 fresh.
- Full-execution positive-gap / zero-pair-repair counts:8/26 archive,3/20 fresh.
- Archive execution26/45/9, fills74 and their64/7/3 contributions, judge240 outputs and194 follow-up flags: checked against included artifacts.
- Fresh agreements9, implementations8, uncertainty11 and latest-plan uncertainty1: checked; these are assistant assessments, not reference labels.
- Independently reran the organizer scorer and exhaustive pair substitutions against all100 original local source episodes: observed scores and pair-repair values matched public tables in100/100 cases. This source-level check requires the original archive, which is not redistributed.
- The six frozen-rule regression tests remain unchanged.
- Bibliographic records and accessible primary abstracts were rechecked. Some full-text endpoints were unavailable; this was not a systematic full-text review. Corrected CAST's full title, distinguished Porter–Zona's1999 publication from its1997 working paper, and supplied Colosseum's full title.

Reproduce the included-artifact checks with `python3 scripts/verify_paper_results.py`. No new API inference calls or behavioral experiments were made. The additional score comparisons are post hoc; frozen rules and predictions were not retuned.
