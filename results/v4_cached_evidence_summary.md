# V4 Cached Evidence Summary

This report is generated from frozen CSV/JSON artifacts. It adds protocol-freeze, citation, rubric, and harsh-reviewer checks without rerunning the expensive experiment suite.

## Global Gates

- submission scorecard rows: `12`
- protocol gates: `12/12`
- rubric axes: `7/7`
- reviewer attacks: `60/60`
- artifact checks: `100`
- in-text citation markers expected after v4 patch: `16`

## Scorecard

- Exact finite audit law: PASS - mean MAE 4.629e-04; max 0.0061 (audit equation only; not the main novelty)
- Raw object-tail collapse: PASS - score gain 0.576; utility drop 0.364; identity error 1.000 (central object-slot binding failure)
- Good-scene negative control: PASS - good utility 0.655; identity error 0.125 (shows high N is not intrinsically harmful)
- Dense and extreme object counts: PASS - dense raw utility 0.036; extreme raw utility 0.026 (stress scope, still synthetic)
- Target retargeting and six-way sweep: PASS - sweep raw utility 0.0001; identity error 1.000 (rules out fixed target-zero artifact)
- Benchmark-style synthetic suite: PASS - raw utility 0.019; combined gain 0.816 (recognized as controlled synthetic stress, not external validation)
- Deployable no-leak repair: PARTIAL - budget-32 gap closure 68.4\% (useful but below 70% strong threshold)
- Support-covered and oracle tiers: PASS - support-covered 91.9\%; oracle 100.0\% (mechanism support and upper bound, not deployment proof)
- Deployment frictions: PASS - gate-vs-raw 0.788; noisy-probe gain 0.867; high-cost gain 0.567 (cost, probe, and fallback stress)
- Learned object-slot artifact: PASS - property margin 0.246; identity margin 0.488; reward corr 0.953 (CPU semi-learned controlled evidence)
- Learned selection and repair transfer: PASS - selection gain 0.658; repair gain 0.823 (object information matters after learning)
- Bootstrap and claim audit: PASS - raw min CI 0.033; repair min CI 0.104 (statistical caution and overclaim guard)

## Protocol

- Code freeze: PASS - v4 build script regenerates cached evidence, compiles the PDF, copies Desktop/repo finals, and writes a manifest.
- Seeds and task families frozen: PASS - Canonical tables cover main, dense, extreme, domain-randomized, counterfactual, target-sweep, synthetic-suite, pilot, probe, and learned variants.
- Metrics frozen: PASS - 100 artifact checks verify required tables, figures, summaries, and schemas.
- Baselines frozen: PASS - Raw high-N, stop-early, random, reward-only, learned identity+reward, observable, combined, support-covered, and oracle rows remain separated.
- Stress conditions frozen: PASS - Dense, extreme, occlusion, crossing, hidden-property, merge/split, target-retargeting, noisy-probe, and probe-cost stresses are generated artifacts.
- Leakage tiers frozen: PASS - Deployable no-leak, support-covered, and oracle tiers are explicit; no-leak C3 stays partial at budget 32.
- Negative controls frozen: PASS - Good-scene controls avoid collapse; hidden-mode unidentifiable controls block high-N rather than claim universal recovery.
- Claim gates frozen: PASS - C1/C2/C4 are strongly supported, C3 is bounded, and C5/C6/C7 remain unsupported nonclaims.
- Paper-claim coverage frozen: PASS - Positive paper claims map only to C1-C4; boundary nonclaims are verified at text locations.
- Citation and related-work pass: PASS - v4 text adds in-text citations for object-centric learning, graph dynamics, planning/world models, calibration, conformal prediction, and benchmark context.
- Harsh-reviewer loop frozen: PASS - 60 reviewer attack rows are generated from the frozen artifacts.
- Final reporting is measurement-only: PASS - v4 synthesis only reads CSV/JSON/PDF artifacts; no final protocol tuning occurs after report generation.

Boundary: v4 remains a controlled synthetic and CPU semi-learned object-centric audit. Real-robot validation, broad external benchmark superiority, and universal repair remain nonclaims.
