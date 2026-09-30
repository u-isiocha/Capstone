# BBO capstone dataset datasheet

Documentation version: 1.0. Snapshot reviewed: 30 September 2026. Related document: [model card](model-card.md).

## Motivation

The project participant assembled this dataset to support sequential black-box optimisation: selecting continuous input vectors that maximise eight unknown scalar objectives while limiting costly evaluations. The dataset combines challenge-provided starting observations with the participant's subsequent queries and returned outputs. It supports learning surrogate models, comparing observed improvements, and explaining exploration versus exploitation decisions in an educational capstone.

The [function descriptions](function-descriptions.docx) supply illustrative applications: source detection, noisy log-likelihood optimisation, compound combinations, warehouse-model tuning, chemical yield, recipe scoring, and six- and eight-dimensional model tuning. These scenarios do not establish that the records are measurements from those industries. Outputs are challenge scores; for example, Function 8 values near 10 must not be labelled validation accuracy on a zero-to-one scale.

## Composition

The distributed snapshot is [data/Capstone.xlsx](../data/Capstone.xlsx), with eight worksheets named `function_1` through `function_8`. Each row contains one query, with numeric columns `input_1` through `input_d` and one scalar `output`. Inputs lie in `[0, 1]`; input units and physical parameter mappings are unspecified. Every objective is maximised, including negative-valued objectives.

| Function | Dimensions | Initial observations | Completed round observations | Total completed | Prepared rows with blank output |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 2 | 10 | 9 | 19 | 1 |
| 2 | 2 | 10 | 9 | 19 | 1 |
| 3 | 3 | 15 | 9 | 24 | 1 |
| 4 | 4 | 30 | 9 | 39 | 1 |
| 5 | 4 | 20 | 9 | 29 | 1 |
| 6 | 5 | 20 | 9 | 29 | 1 |
| 7 | 6 | 30 | 9 | 39 | 1 |
| 8 | 8 | 40 | 9 | 49 | 1 |
| Total | — | 175 | 72 | 247 | 8 |

There are 255 query rows, excluding headers. The original data are also retained as 16 NumPy `.npy` files under [data/initial](../data/initial): one input array and one output array per function. The leading workbook observations match these initial arrays. No input cells are missing and no exact duplicate vectors occur within a sheet in this snapshot. The eight missing outputs belong to prepared round 10, at Excel rows 21, 21, 26, 41, 31, 31, 41 and 51 respectively. They are excluded from all reported performance metrics.

Coverage is deliberately uneven because queries respond to earlier results. Function 1 remains nearly uninformative; Function 2 is explicitly noisy; the higher-dimensional functions have sparse coverage. The workbook has no per-query timestamps, submission receipts, noise replicates at identical inputs, or run-configuration columns. The initial sampling procedure and evaluation-system internals are not recorded.

## Collection process

Initial observations were supplied with the challenge. The participant then selected one vector per function in each round, obtained scores from the challenge evaluator, and recorded those outputs in the workbook. The participant confirms the following script attribution:

- Rounds 1–6: `Capstone.py`, a scikit-learn Gaussian process with UCB selection. Its surviving implementation searches within observed coordinate ranges, using a grid in two dimensions and Sobol candidates above two dimensions.
- Rounds 7–9: `Capstone_best_attempt.py`, an ensemble of three RBF Gaussian-process surrogates selected from nine length scales using leave-one-out error, with full-domain random candidates and local refinement.
- Round 10 preparation: `Capstone_sklearn_improved.py`, using an ARD RBF Gaussian process, learned noise, global Sobol coverage, multi-scale local candidates and function-specific acquisition policies. The repository implementation is [src/optimizer.py](../src/optimizer.py).

The [model card](model-card.md) distinguishes surviving script settings from historically verified execution details. Per-round code snapshots and seeds for rounds 1–9 are unavailable, so exact historical regeneration cannot be promised.

The persistent workspace budget records **10 used and 3 remaining rounds out of 13**: nine completed rounds plus appended round 10 with outputs pending. A complete round is charged immediately when its eight query rows are appended; later submission or output entry does not charge it again. This document is a dated snapshot, not the authoritative budget counter.

## Preprocessing and uses

The workbook preserves raw returned outputs. The current optimiser excludes blank outputs, checks the completed inputs against `[0, 1]`, and fits each function separately. Inputs already use the challenge's normalised domain; no physical-unit conversion is inferred. Function 5 outputs are transformed with the natural logarithm during fitting, requiring strictly positive values. Gaussian-process targets are then normalised internally. Other functions retain their supplied output scale before normalisation; negative objectives are not negated again.

Candidate generation clips local perturbations to `[0, 1]`, rounds candidate-pool coordinates to 12 decimals for deduplication, and rejects vectors matching completed inputs within an absolute tolerance of `1e-9`. Displayed vectors use six decimal places. Round-10 saved inputs use those displayed values, except for the recorded manual override. Readers should use workbook precision for analysis rather than copying rounded vectors from the model card.

Intended uses include educational optimisation, retrospective learning-curve analysis, surrogate development and auditing query decisions. Comparisons should account for adaptive sampling and the shared evaluation budget. Inappropriate uses include treating the records as a representative population sample, claiming a global optimum, inferring causal physical mechanisms, presenting the scores as actual medical or safety outcomes, or deploying real-world process settings directly from these normalised coordinates. Random train/test splits alone do not validate a sequential optimisation policy; future evaluations or separately designed benchmark experiments are needed.

## Distribution and maintenance

The dataset is available in this repository at [data/Capstone.xlsx](../data/Capstone.xlsx), with [initial arrays](../data/initial) and [challenge descriptions](function-descriptions.docx). The workbook snapshot was refreshed from the working dataset when this documentation was prepared, including completed round 9 and blank-output round 10.

## Evidence and traceability

Counts and results were checked against every sheet of the working workbook and the original NumPy arrays. The workspace `evaluation_budget.json` provides round-to-row mappings for rounds 1–10. The participant supplied the script-to-round attribution on 30 September 2026. Earlier scripts survive under workspace `archive/optimisers/2026-09-29/`; they are not distributed in this repository. The performance table and its calculation definitions are in the [model card](model-card.md).
