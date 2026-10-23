Current snapshot (23 October 2026): all 13 allocated rounds have completed outputs; 279 observations, none pending. Budget: 13 used, zero remaining. See [final results](final-results.md). The distributed ledger mirrors the workspace ledger, which still labels round 13 as pending; the workbook confirms completion. Earlier dated discussion below is historical.

# Optimisation methodology

Separate ARD RBF Gaussian processes with learned noise fit completed observations only. Function 5 uses log outputs. Sobol global candidates and multiscale local perturbations support UCB, EI or posterior-mean selection.

Round-11 review: eleven completed rounds, two remaining before round 12 preparation. The executable policy now reads the remaining budget: at two or fewer remaining rounds, Function 3 uses EI within distance 0.15 of its best point after two weak boundary probes; Function 6 tightens refinement to distance 0.08; Functions 7 and 8 use UCB coefficient 0.35 within distance 0.20 of their improving incumbents. Function 1 retains exploratory UCB because its surface remains uninformative. Function 2 retains near-best noise validation. Function 5 retains posterior mean within distance 0.02 to 0.10; its latest inward perturbation was below the corner maximum. Function 4 retains its trend-based policy.

[Round-11 preparation](round11-preview.md) is historical. The final-two-round acquisition and radius changes are now implemented in both optimiser scripts; other policy rules remain trend-based. Predictions remain unverified.

All eight sheets must pass validation before append. Pending outputs or duplicates withhold the whole round. Appending preserves formatting and charges the round immediately once. Preview consumes no budget. Repository snapshots refresh on query requests; the workspace ledger remains authoritative.
