# Repository structure

```text
repository/
├── README.md                         # Project overview and reproducible run instructions
├── requirements.txt                  # Runtime dependencies
├── src/
│   └── optimizer.py                  # Active BBO recommendation script
├── data/
│   ├── Capstone.xlsx                 # Current query histories for functions 1-8
│   └── initial/                      # Original input/output NumPy arrays by function
├── docs/
│   ├── function-descriptions.docx    # Challenge definitions and BO guidance
│   ├── methodology.md                # Modelling strategy and evidence limits
│   ├── datasheet.md                  # Dataset provenance, composition and maintenance
│   ├── model-card.md                 # Ten-round approach, results and limitations
│   └── repository-structure.md        # Layout and reproducibility rules
├── notebooks/                         # Optional exploratory analysis, kept separate from source
└── results/                           # Generated figures and tables; do not overwrite raw data
```

The repository deliberately excludes temporary Office files, Python caches, stale workbook copies, experimental scripts, and inspection exports. Store future analysis notebooks in `notebooks/`, generated figures and tables in `results/`, and reusable data queries in `src/` or `scripts/` when they are added.

## Reproducibility rules

- Keep evaluated inputs and outputs in `data/Capstone.xlsx`; do not replace completed outputs.
- Run the optimiser with an explicit `--seed` whenever a recommendation must be reproduced.
- Use `--no-append` to preview recommendations without changing the workbook.
- Record externally supplied output-only observations in documentation or the script's benchmark mapping, never as a workbook row without its input vector.
