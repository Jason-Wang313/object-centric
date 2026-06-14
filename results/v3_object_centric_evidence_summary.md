# V3 Object-Centric Evidence Summary

This file is generated from cached audited artifacts. It does not rerun the full experiment suite.

## Core Claim Status

- C1: strongly_supported
- C2: strongly_supported
- C3: partial
- C4: strongly_supported
- C5: unsupported
- C6: unsupported
- C7: unsupported

## Submission Scorecard

- C1 / finite tie-aware selected-utility law: 0.000463 (strongly_supported)
- C2 / raw selected-tail object binding collapse: score gain 0.576; utility drop 0.364; identity error 1.000 (strongly_supported)
- C2 / good-scene negative control: utility 0.655; identity error 0.125 (strongly_supported)
- C2 / dense and extreme object-count collapse: dense raw utility 0.036; extreme raw utility 0.026 (strongly_supported)
- C2 / retargeting and target-identity sweep: target-sweep raw utility 0.0001; identity error 1.000 (strongly_supported)
- C3 / deployable no-leak pilot-label LCB repair: 68.4\% (partial)
- C3 / support-covered repair: budget 32 91.9\%; budget 128 91.9\% (strong_controlled_support)
- C3 / observable repair and ablation: observable gain 0.880; combined vs best single 0.277 (strong_controlled_support)
- C3 / deployment gate policy simulation: vs raw 0.788; vs stop-early 0.537; min win 93.8\% (strong_controlled_support)
- C3 / pilot, noisy-probe, probe-cost stress: pilot gain 0.819; noisy-probe gain 0.867; high-cost gain 0.567 (strong_controlled_support)
- C4 / CPU NumPy learned object-slot model: property margin 0.246; identity margin 0.488; reward corr 0.953 (strongly_supported)
- C4 / learned selection and learned repair transfer: identity vs raw 0.658; repair vs raw 0.823; repair vs learned identity 0.225 (strongly_supported)

## 50-Round Self-Attack

- rounds: 50
- status counts: {'bounded': 4, 'pass': 46}
- reviewer angles: {'theory novelty': 1, 'novelty': 2, 'external validity': 1, 'overclaim': 3, 'mechanism': 4, 'scope': 2, 'scale': 1, 'negative control': 1, 'theory validation': 1, 'theory detail': 1, 'leakage': 5, 'claim strength': 3, 'probe realism': 2, 'policy': 1, 'baseline': 1, 'ablation': 1, 'statistics': 2, 'calibration': 1, 'safety': 1, 'learned evidence': 7, 'comparison': 1, 'audit': 1, 'reproducibility': 3, 'workflow': 1, 'presentation': 1, 'framing': 2}
