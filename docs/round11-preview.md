# Round 11 query preview

Reviewed 4 October 2026. Reproduced with `Capstone_sklearn_improved.py --no-append --seed 20261004`, default candidate counts and eight restarts. Round 11 appended on 4 October 2026: 11 rounds used and 2 remaining. All eight outputs are pending. External submission is not confirmed.

## Queries

```text
function_1: 0.520172-0.663415
function_2: 0.696034-0.884694
function_3: 0.999523-0.005175-0.003177
function_4: 0.406048-0.387633-0.441103-0.414129
function_5: 0.979976-1.000000-1.000000-1.000000
function_6: 0.453309-0.206994-0.563126-0.951546-0.048233
function_7: 0.178163-0.153437-0.412489-0.303783-0.325260-0.651742
function_8: 0.125164-0.146103-0.168096-0.157473-0.825605-0.491306-0.208638-0.710442
```

## Current best observations

- Function 1: 7.710875115e-16 at 0.731024-0.733000.
- Function 2: 0.6179045161 at 0.697478-0.904235.
- Function 3: -0.007314340245 at 0.354743-0.363015-0.488141.
- Function 4: 0.4194697964 at 0.432354-0.363441-0.434507-0.379812.
- Function 5: 8662.4825 at 1.000000-1.000000-1.000000-1.000000.
- Function 6: -0.2631844133 at 0.483352-0.295892-0.619378-0.903924-0.127876.
- Function 7: 3.215413564 at 0.202001-0.238791-0.473174-0.273631-0.295676-0.674048.
- Function 8: 9.965400453 at 0.134266-0.132984-0.150188-0.041549-0.938880-0.487463-0.260925-0.732389.

## Policy review

- Function 1: exploratory UCB 3.0; readings remain essentially uninformative.
- Function 2: EI 0.01 within distance 0.02 of the best point; nearby validation is justified by noisy lower recent readings, although distinct points cannot isolate noise.
- Function 3: exploratory UCB 2.5; round 10 worsened to -0.140534 and the current best still trails -0.00551. Another basin remains worth exploring with three rounds left.
- Function 4: EI 0.005; round 10 recovered to 0.348839 but remains below the best, supporting further refinement.
- Function 5: posterior mean within distance 0.02–0.10 of the best. The evaluated all-one corner improved markedly. A negligible near-duplicate was rejected in the review; the final query probes sensitivity nearby.
- Function 6: EI 0.005 within distance 0.15 of the best; round 10's -0.885754 boundary result supports local refinement. Its predicted -0.074173 remains unverified.
- Function 7: mixed UCB 0.75; the new best supports refinement with cautious exploration on the sparse six-dimensional surface. Predicted 3.317212 is unverified.
- Function 8: local posterior mean within distance 0.25; round 10 made only a small improvement, consistent with a plateau. Predicted 10.004537 is unverified.

The policy review is manual, not an automatic budget schedule. Executable corrections in both optimisers affect Functions 5 and 6; round-10 evaluated inputs remain unchanged. Syntax checks and the full seeded preview passed. Displayed queries are rounded to six decimals and remain non-duplicate, within bounds and compliant with the reviewed distance limits. Round 11 was appended at rows 22, 22, 27, 42, 32, 32, 42 and 52 for Functions 1–8. Saved inputs, blank outputs and copied formatting were verified.
