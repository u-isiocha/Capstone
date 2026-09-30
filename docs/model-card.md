# BBO optimisation model card

Documentation version: 1.0. Reviewed: 30 September 2026. Dataset: [datasheet](datasheet.md).

## Overview

**Name:** Function-specific Gaussian-process Bayesian optimisation for the BBO capstone. **Type:** sequential, surrogate-assisted maximisation of eight continuous black-box objectives. **Implementation version:** the round-10 scikit-learn implementation reviewed on 30 September 2026, distributed as [src/optimizer.py](../src/optimizer.py); the active workspace filename is `Capstone_sklearn_improved.py`. No tagged software release or persisted fitted-model version is supplied. A separate Gaussian process is refitted for each function from its completed observations.

The ten-round narrative covers **nine completed rounds and one prepared round**. Round-10 performance is not yet available. The budget ledger records 9 used and 4 remaining rounds from an allocation of 13; that allocation is distinct from the ten rounds covered here.

## Intended use

The approach selects the next vector in `[0, 1]^d`, for dimensions 2–8, when objective evaluations are more expensive than surrogate fitting. It supports educational experimentation, limited-budget query selection, and transparent review of exploration and exploitation. Its outputs are candidate vectors, forecasts and diagnostics, rather than certified optimal settings.

Avoid using it unchanged for categorical or integer variables, multi-objective trade-offs, unbounded domains, safety-constrained experiments, causal inference, or production qualification. The challenge narratives do not supply the physical constraints needed for medical, industrial or environmental deployment. It does not train an SVM or neural network.

## Strategy across ten rounds

Script attribution below is confirmed by the participant. Technical settings describe the surviving scripts; these are not immutable copies of each historical run. In particular, the archived second script contains a review made after round 9. Results cannot prove that every surviving setting was used unchanged in rounds 7–9.

### Rounds 1–6: initial GP and UCB search

`Capstone.py` used scikit-learn `GaussianProcessRegressor` with a constant-times-RBF kernel, one shared length scale across dimensions, output normalisation, `alpha=1e-6`, and ten kernel-optimiser restarts. The executed loop selects UCB for every function, even though the file also defines EI and PI and an unused acquisition mapping. The surviving UCB multipliers for Functions 1–8 are `2, 1, 5, 2, 2, 2, 0.1, 0.1`.

Search was restricted to each coordinate's observed minimum and maximum. Two-dimensional functions used a Cartesian grid; higher-dimensional functions used 4,096 Sobol points. This offered uncertainty-aware exploration within known bounds but could miss unexplored boundary regions. The script also discarded the final row unconditionally, assuming it was unfinished; a completed final row would therefore have been omitted. It wrote a separate `Capstone2.xlsx` and lacked the current append checks. Historical random seeds are not recorded.

### Rounds 7–9: wider search and GP ensemble

`Capstone_best_attempt.py` broadened the candidate domain to the full unit cube. It standardised targets, fitted isotropic RBF surrogates at nine length scales from `0.04` to `0.50`, selected the three lowest leave-one-out losses, and averaged their predictions using inverse-loss weights. A fixed `1e-6` nugget provided numerical stabilisation rather than learned observation noise. Function 5 was fitted in natural-log output space.

The candidate pool contained 100,000 uniform global points plus 30,000 local perturbations at each of five radii (`0.20`, `0.10`, `0.05`, `0.025`, `0.01`) around the best observation. The surviving post-round-9 policy uses UCB multipliers 2.0 and 1.5 for Functions 1 and 3, and posterior mean for the others. Blank-output filtering, seeded previews, duplicate checks and formatting-preserving appends improved the workflow. Averaging component standard deviations is a heuristic and omits between-model disagreement; it is not a fully calibrated mixture uncertainty.

### Round 10: ARD, learned noise and targeted acquisition

The current implementation returns to scikit-learn with `ConstantKernel * RBF + WhiteKernel`, a separate learned RBF length scale for every coordinate, `normalize_y=True`, eight optimiser restarts and numerical jitter `alpha=1e-10`. Length-scale bounds are `0.01–2.0`. Function 2 has noise-level bounds `1e-5–2.0`; other functions use `1e-8–0.10`.

The default pool combines 65,536 scrambled Sobol points with approximately 12,000 local points **per radius**, shared across the three strongest observations, at the same five radii. Function 2 adds 12,000 near-incumbent points with perturbation standard deviation `0.005`. Local points are clipped to the unit cube and duplicates removed.

The saved preview used seed `20260929`, defaults and the completed round-9 data. Its selected policies were:

| Function | Round-10 selection | Evidence and rationale |
| --- | --- | --- |
| 1 | UCB, multiplier 3.0 | All nine new outputs remain below the tiny initial best; broad uncertainty-led exploration remains appropriate. |
| 2 | EI, margin 0.01; distance ≤0.02 from incumbent | The noisy sequence declined in rounds 7–9; nearby validation targets the promising region. |
| 3 | UCB, multiplier 2.5 | Round 8 improved the best, but the recorded benchmark `-0.00551` is still higher; another basin may be better. |
| 4 | EI, margin 0.005 | The best occurred in round 7, followed by two lower positive scores; EI balances predicted improvement and uncertainty. |
| 5 | Posterior mean; distance ≤0.10 from incumbent | Round 9 improved yield to 4367.74, above the recorded benchmark 2883.2; local refinement was proposed. |
| 6 | EI, margin 0.005 | The best remains round 6; rounds 7–9 deteriorated. The current fixed fallback still uses EI and needs continued review. |
| 7 | UCB, multiplier 0.75 | Round 9 established a new best, while six-dimensional coverage remains sparse. |
| 8 | Posterior mean; distance ≤0.25 from incumbent | Outputs have clustered near the round-5 best, supporting local refinement. |

Distances are Euclidean in normalised input space. The restrictions apply when the candidate pool contains eligible points. EI for Functions 4 and 6 searches the mixed global/local pool; it is not a hard local constraint. Function 2 uses ordinary EI with a noisy GP, not a dedicated noisy-EI acquisition. Nearby distinct points do not isolate observation noise as exact repeated evaluations would.

Round-10 stored vectors are in the final rows of [the workbook](../data/Capstone.xlsx). Function 5 is an explicit participant override, `1-1-1-1`, rather than the proposed `1.000000-0.396840-1.000000-1.000000`. All eight outputs remain blank. This round therefore provides evidence of query preparation, not improved performance.

Policy review is manual and ongoing. The executable chooses among fixed function rules, a recent-output heuristic and benchmark comparisons; it does **not** read the remaining budget or automatically schedule exploration across rounds. With four rounds remaining in the ledger, the reviewed policy retains exploration for weak signals and refinement for stronger regions, but that rationale is not an implemented budget controller.

## Performance

The primary metric is **best observed output**, including initial observations, after round 9. Absolute gain is `best after round 9 − best initial output`. Best-so-far trajectories track sample efficiency against completed rounds. Scores remain on each function's native scale; averaging them across functions would be misleading. No held-out prediction score, calibrated interval coverage, global regret, or multi-seed policy comparison is established.

| Function | Initial best | Best through round 9 | Absolute gain | Best first observed |
| --- | ---: | ---: | ---: | --- |
| 1 | 7.710875115e-16 | 7.710875115e-16 | 0 | Initial data |
| 2 | 0.6112052158 | 0.6179045161 | 0.00669930035 | Round 5 |
| 3 | -0.03483531335 | -0.007314340245 | 0.02752097310 | Round 8 |
| 4 | -4.025542282 | 0.4194697964 | 4.445012078 | Round 7 |
| 5 | 1088.859618 | 4367.735751 | 3278.876133 | Round 9 |
| 6 | -0.7142649478 | -0.2631844133 | 0.4510805345 | Round 6 |
| 7 | 1.364968304 | 2.976688912 | 1.611720608 | Round 9 |
| 8 | 9.598482003 | 9.962234961 | 0.3637529581 | Round 5 |

Seven functions improved on their initial best. Function 1 did not. Function 2's small best-value gain is not proof of an improvement in its expected score because its output is noisy. Function 5 and Function 7 made their largest recorded gains during the later phase, but the sequence is not a controlled comparison of algorithms: later scripts also benefited from more observations.

Best observed input vectors, rounded to six decimals for display:

```text
function_1: 0.731024-0.733000
function_2: 0.697478-0.904235
function_3: 0.354743-0.363015-0.488141
function_4: 0.432354-0.363441-0.434507-0.379812
function_5: 1.000000-0.439581-1.000000-0.984070
function_6: 0.483352-0.295892-0.619378-0.903924-0.127876
function_7: 0.194826-0.252583-0.390347-0.224822-0.269204-0.655437
function_8: 0.098358-0.088644-0.130160-0.072470-0.778659-0.616865-0.263082-0.847796
```

These correspond to Excel rows 4, 16, 24, 38, 30, 27, 40 and 46. Stored precision, not the rounded display, defines the evaluated vector. The underlying dataset contains 247 completed observations: 175 initial observations and 72 from nine eight-function rounds. No round-10 result is included.

## Assumptions and limitations

- The GP assumes a smooth response with distances meaningful on continuous normalised coordinates. Sharp isolated peaks, discontinuities, changing objectives and categorical encodings can violate that model.
- The RBF kernel, sparse coverage and limited candidate pool can miss a global optimum. ARD length scales are fitted model parameters, not causal feature importance.
- Learned noise does not establish calibrated uncertainty. GP predictive standard deviations include the white-noise term; noise can affect acquisition as well as forecasts. Selecting the largest noisy observation may overstate achievable expected performance.
- The trend heuristic compares blocks of six observations and uses scale-based thresholds. Early blocks may mix initial and sequential observations. Its Function 2 label “noisy and recently worsening” is triggered by recent spread and does not independently test a downward trend. Function 6's recent deterioration illustrates why human review remains necessary.
- Function 5's back-transformed centre is `exp(log-space mean)`, a median under a log-normal interpretation, not the log-normal expectation. Its reported uncertainty uses a delta approximation. Acquisition is calculated in log space, although performance is reported on the original scale.
- Forecasts beyond all observed scores are unverified extrapolations. Neither a positive Function 6 forecast nor a tiny Function 1 response proves an attainable optimum.
- The script blocks automatic duplicate appends, so exact noise replication requires a separately controlled workflow. Per-sheet append guards do not enforce all-or-nothing round preparation, submission status, or the total budget.
- Earlier run environments and seeds are incomplete; dependencies in `requirements.txt` are not version-pinned. Replaying the current algorithm is more reproducible than reconstructing every historical query.

## Transparency, reproducibility and ethical considerations

Publishing the data schema, evaluated vectors, raw outcomes, actual acquisition logic, missing outputs and manual overrides makes decisions auditable. Reporting native-scale results and unsuccessful rounds avoids selective success claims. Distinguishing observations from forecasts prevents optimistic surrogate outputs from being presented as confirmed results.

The challenge records do not contain demographic attributes; no group-fairness evaluation has been performed. Real-world adaptation would require domain-specific constraints, appropriate noise replication, prospective validation, and assessment of who bears the costs or harms of experiments. A favourable challenge score cannot establish medical efficacy, safe source detection, or a qualified process setting. Data-sharing permissions must also be resolved as described in the datasheet.

To reproduce the current candidate-generation procedure from the repository root:

```powershell
python -m pip install -r requirements.txt
python src/optimizer.py --no-append --seed 20260929 --n-global 65536 --n-local 12000 --restarts 8
```

The saved round-10 preview used the equivalent workspace script. This command is a replay recipe, not a claim that a new preview was executed during documentation. The prepared blank-output rows are excluded from fitting; their presence blocks appending. The Function 5 manual override must not be attributed to the replay. Record package versions, source revision and workbook checksum alongside future previews to improve repeatability.

For independent metric verification, take the maximum completed output in each sheet; compare it with the maximum of the corresponding [initial output array](../data/initial). With `n_initial` given in the datasheet, round `r` is Excel row `n_initial + r + 1`, accounting for the header. The current results use rounds 1–9 only.

Maintainer: the capstone project owner; public contact and release terms remain unspecified. Refresh this card after each completed evaluation and any substantive policy change. Supporting evidence consists of the [workbook](../data/Capstone.xlsx), [function descriptions](function-descriptions.docx), [current implementation](../src/optimizer.py), the participant's script attribution, and the workspace budget, archived scripts and round-10 preview identified in the [datasheet](datasheet.md).
