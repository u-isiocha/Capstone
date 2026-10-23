# Round 12 preparation

Prepared 2026-10-11 using active optimiser preview seed 20261011, 65,536 global candidates, 12,000 local candidates per radius, eight GP restarts. Preview passed; displayed six-decimal vectors were rechecked by the whole-round append safeguards and saved to both workspace workbooks. Budget: 12 used, one remaining. Outputs pending. No external submission performed.

Rows: Functions 1/2: 23; Function 3: 28; Functions 4/7: 43; Functions 5/6: 33; Function 8: 53.

## Queries and evidence

- Function 1: `0.464422-0.940064`. Exploratory UCB 3.0; no useful positive signal. Best 7.710875114502849e-16 at `0.731024-0.733000`.
- Function 2: `0.695952-0.884535`. EI 0.01 within 0.02 of best; nearby validation of a noisy region, not an exact replicate. Latest output recovered to 0.6036575606. Best 0.6179045161 at `0.697478-0.904235`.
- Function 3: `0.491639-0.371787-0.433512`. EI 0.001 within 0.15 of best; boundary probes worsened to -0.1405343 and -0.1863594. Best -0.007314340245 at `0.354743-0.363015-0.488141`.
- Function 4: `0.405641-0.384772-0.441708-0.412950`. EI 0.005; recent local outputs remain below the maximum. Best 0.4194697964 at `0.432354-0.363441-0.434507-0.379812`.
- Function 5: `1.000000-0.979984-1.000000-1.000000`. Local posterior mean, distance 0.02–0.10. Latest inward step yielded 8289.95088 below 8662.4825 at `1.000000-1.000000-1.000000-1.000000`; refine another direction.
- Function 6: `0.472263-0.302729-0.637005-0.854843-0.182676`. EI 0.005 inside tightened radius 0.08 after multiple weaker queries. Best -0.2631844133 at `0.483352-0.295892-0.619378-0.903924-0.127876`.
- Function 7: `0.185123-0.198891-0.485108-0.336710-0.316019-0.676140`. UCB 0.35 within 0.20 of improving best 3.244774840 at `0.178163-0.153437-0.412489-0.303783-0.325260-0.651742`.
- Function 8: `0.132284-0.195305-0.086314-0.196172-0.822777-0.513534-0.207928-0.673031`. UCB 0.35 within 0.20 of latest best 9.992536231 at `0.125164-0.146103-0.168096-0.157473-0.825605-0.491306-0.208638-0.710442`. Recent small improvements justify continued local refinement despite the generic trend classifier calling the region a plateau.

## Verification and limitations

Both scripts passed syntax checks. The seeded preview exercised the final-two-round policy and local restrictions. Both saved workbooks match; all eight new outputs are blank, row styles match preceding rows, and round 11 outputs agree within Excel floating-point precision. The exact-value comparison initially failed due to numeric serialization; numeric verification passed. The ledger charges round 12 exactly once, and repository workbook/budget snapshots were refreshed.

Predicted improvements for Functions 3, 7 and 8 require evaluation. The Function 3 prediction near zero is particularly uncertain relative to its observed best. High-dimensional observations remain sparse; no global optimum is established. These policy changes affect the round 12 candidates; previous round 11 inputs and evaluations are retained.
