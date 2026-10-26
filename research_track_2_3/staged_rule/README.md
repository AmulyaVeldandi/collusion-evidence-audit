# Rule package ready for a new test set

Start with PROTOCOL.md and config.json. rule.py implements the staged verdict and two baselines. annotation_template.json lists required evidence. Preserve source citations and keep test references separate from predictions. Do not use old80 labels/roles as ground truth.

Reproduce local application:

    python3 research_track_2_3/staged_rule/apply_development.py
    python3 -m unittest discover -s research_track_2_3/staged_rule -p 'test_*.py'

The content freeze covers the deterministic evidence rule, configuration, annotation template and protocol. It does NOT claim a frozen new API annotation procedure: the previous all80 judge schema does not independently assess expressed harmful purpose P and cannot be silently substituted for this template. Any future judge prompt/model/settings must be specified and locked before access to the new test set. No new API calls or generation are performed by this package.

Next required input: the new test episodes and independently prepared reference annotations, with scenario/seed IDs for grouped reporting. Merely generating assigned colluders does not create verified harmful-collusion ground truth.
