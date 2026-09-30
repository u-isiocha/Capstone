# Optimisation methodology

## Surrogate model

`src/optimizer.py` fits a separate scikit-learn `GaussianProcessRegressor` to each function's completed observations. Blank outputs are excluded. The covariance model is a constant kernel multiplied by an ARD RBF kernel, so every input dimension receives its own optimised length scale. A `WhiteKernel` estimates observation noise, with wider noise bounds for noisy Function 2. Outputs are normalised and kernel hyperparameters are fitted with multiple optimiser restarts.

Function 5 is fitted in log-output space to stabilise its large positive scale. Printed forecasts are transformed back to the workbook scale and remain surrogate estimates, not observations.

## Candidate search and acquisition

The candidate pool combines scrambled Sobol coverage of `[0, 1]^d` with perturbations at radii `0.20`, `0.10`, `0.05`, `0.025`, and `0.01` around the three strongest observations. Exact duplicate vectors are removed.

Acquisition is reassessed from the current observations:

- Function 1 uses high-UCB exploration because its completed outputs remain essentially uninformative.
- Function 2 estimates noise and restricts EI to non-duplicate near-repeats when recent results are noisy.
- Function 3 uses UCB while its output-only benchmark exceeds the workbook maximum.
- Function 5 uses UCB only when an external benchmark exceeds the observed maximum. Otherwise, it exploits posterior mean inside a local trust region.
- Function 4 uses moderate UCB after deterioration and EI otherwise.
- Functions 7 and 8 use cautious UCB while trends remain mixed, then local posterior-mean refinement when a strong basin plateaus.
- Other stable functions use EI for local refinement.

The script reports the fitted kernel, current best observation, trend diagnosis, candidate, acquisition type, predictive uncertainty, and a caveat whenever the forecast exceeds all observed outputs.

## External evidence and safeguards

Output-only external observations are benchmarks, never training rows. The recorded benchmarks are `-0.00551` for Function 3, `2883.2` for Function 5, and `9.9369` for Function 8. The workbook observations currently exceed the Function 5 and Function 8 benchmarks, while Function 3 still warrants broader exploration.

Append mode never overwrites outputs, never treats blanks as zero, and never appends when a sheet's final output is blank. It blocks duplicate vectors, copies the previous row's formatting, and does not resave the workbook when every recommendation is withheld. Use `--no-append` for preview and `--seed` for reproducibility.

## Limitations

An RBF GP assumes a smooth response and may extrapolate poorly in sparse or high-dimensional regions. Learned length scales or noise levels at their bounds are diagnostic warnings rather than proof of feature relevance. Function 2 still requires repeated validation, and no surrogate prediction establishes a global optimum until the black box is evaluated.
