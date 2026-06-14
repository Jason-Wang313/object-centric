# Claims

## Supported

- Exact finite tie-aware score-tail laws predict selected utility on finite object-candidate populations.
- Controlled object-centric scenes show selected-tail binding failure where object score can increase while real utility stagnates or falls; the good-scene negative control avoids the same collapse, and dense, extreme object-count, synthetic task-suite, and target-identity sweep variants reproduce the corrupted-setting failure.
- Pilot-label calibrated lower-confidence selection reduces selected-tail hallucination in controlled support-covered regimes. The generated artifacts explicitly separate deployable no-leak selectors, support-covered probe/simulator diagnostics, and oracle upper bounds, and the main repair claim is downgraded to partial unless nested final-test split robustness clears the no-leak thresholds. The controlled repair evidence includes identity consistency, hidden-property calibration, targeted probing, observable-only repair, pilot-label calibration, combined repair, paired seed gains, bootstrap confidence checks, repair ablations, seed-block robustness, score-noise sensitivity, noisy-probe reliability stress, probe-cost sensitivity, dense-object OOD stress, extreme 10/12-object stress, benchmark-style synthetic task-suite stress, deployment-gate policy simulation, held-out domain-randomized stress, counterfactual target-swap stress, multi-target identity sweep stress, pilot-label budget sensitivity, leave-one-failure-out pilot calibration, toy model-family proxy diagnostics, and a high-N stress panel.
- A CPU NumPy semi-learned object-centric model improves property, identity-alignment, and transition prediction over simple baselines on generated trajectories, with feature ablations, held-out dense/occluded/crossing synthetic domain-shift checks, learned selection transfer, and conservative learned repair-policy transfer showing object information matters. The learned repair-policy transfer is judged by mean paired gain, bootstrap lower bounds, strict wins, non-loss rate, and bounded worst seed-level loss against the learned identity+reward selector.

## Unsupported

- Real-robot validation.
- Broad benchmark superiority over graph physics, latent dynamics, or diffusion world models; the toy proxy panel is only a controlled diagnostic comparison.
- Universal repair, universal object learning, guaranteed 100% recovery, or general robotic reliability. The hidden-mode negative control is an explicit impossible case where indistinguishable observables must block high-N rather than promise recovery.

The executable audit writes the machine-readable version to `results/claims_status.json` and the paper-claim coverage matrix to `docs/paper_claim_coverage.md`, `results/paper_claim_coverage.json`, and `results/tables/paper_claim_coverage.csv`. Core claims are `strongly_supported` only if numeric thresholds in the generated claim-strength record pass, required artifacts verify, artifact hashes are written, positive paper claims map to strongly supported audit rows with verified cited locations, and paper text avoids supported overclaims.
