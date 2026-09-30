# Black-box optimisation capstone

This project recommends the next input vector for eight unknown functions while minimising expensive black-box evaluations. Each function accepts continuous inputs in `[0, 1]` and returns one scalar output; the objective is maximisation. Function dimensionality ranges from 2 to 8.

## Repository layout

Read the [dataset datasheet](docs/datasheet.md) for provenance, composition, permitted-use gaps and maintenance, and the [model card](docs/model-card.md) for the ten-round strategy and verified results. The documented snapshot contains nine completed rounds and prepared round-10 inputs with blank outputs.

See [the repository structure](docs/repository-structure.md). The active optimiser is `src/optimizer.py`, the current evaluation history is `data/Capstone.xlsx`, and the challenge definitions are in `docs/function-descriptions.docx`.

## Setup

Create an environment and install the runtime dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the optimiser

Preview recommendations without changing the workbook:

```powershell
python src/optimizer.py --no-append --seed 20260825
```

To append an eligible recommendation, omit `--no-append`. The script appends only when the prior row in that function's sheet has a completed output, preserves the row formatting, and leaves the new output blank for the next black-box evaluation.

## Inputs and outputs

`data/Capstone.xlsx` contains one sheet per function (`function_1` to `function_8`). Each sheet has `input_1` through `input_n` and an `output` column. Blank outputs are pending evaluations, not zero-valued observations, and are excluded from model fitting.

## Approach and current strategy

The optimiser uses scikit-learn Gaussian-process regression with an ARD RBF kernel, output normalisation, learned observation noise, and multiple kernel-optimiser restarts. It searches Sobol global candidates together with progressively finer perturbations around the three strongest completed observations.

- `function_1` and `function_3` use uncertainty-led UCB exploration when observations or benchmarks indicate that the current basin is insufficient.
- `function_2` uses a learned `WhiteKernel` noise term and noise-aware near-best EI candidates. Exact duplicate rows are still blocked automatically.
- `function_5` is fitted in log-output space. Because the observed maximum exceeds its recorded output-only benchmark, posterior-mean exploitation is restricted to a local trust region around the incumbent.
- Higher-dimensional functions use a trend-aware choice between cautious UCB and local posterior-mean refinement. Surrogate forecasts above every observed output are explicitly flagged as uncertain.

Read [the methodology notes](docs/methodology.md) for modelling details, external evidence, and limitations.

## Reproducibility and limitations

Use `--seed` for repeatable candidate generation. Candidate counts and kernel restart counts are configurable with `--n-global`, `--n-local`, and `--restarts`. Do not claim an optimum from a surrogate prediction: only an evaluated black-box output confirms a result. The current approach does not train an SVM or neural network.
