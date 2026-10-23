# Round 13 preparation

Prepared 18 October 2026. All round 12 outputs completed. Round 13 appended as a complete eight-function round; 13 used, zero remaining. Outputs pending; external submission not performed.

Reproduced with `python Capstone_sklearn_improved.py --no-append --seed 20261018`, default 65,536 global candidates, 12,000 local candidates per radius and eight restarts. Six-decimal inputs below passed append validation.

- function_1: `0.251520-0.982174`; row 24. Best 7.7108751145e-16 at `0.731024-0.733000`.
- function_2: `0.695402-0.864791`; row 24. Best 0.749983544284 at `0.695952-0.884535`.
- function_3: `0.494639-0.357146-0.435933`; row 29. Best -0.00731434024537 at `0.354743-0.363015-0.488141`.
- function_4: `0.406405-0.384232-0.437835-0.410057`; row 44. Best 0.419469796362 at `0.432354-0.363441-0.434507-0.379812`.
- function_5: `0.980631-0.995005-1.000000-1.000000`; row 34. Best 8662.4825 at `1.000000-1.000000-1.000000-1.000000`.
- function_6: `0.459486-0.322472-0.612069-0.881591-0.189018`; row 34. Best -0.263184413327 at `0.483352-0.295892-0.619378-0.903924-0.127876`.
- function_7: `0.242007-0.144408-0.543271-0.274368-0.309410-0.668399`; row 44. Best 3.24477483985 at `0.178163-0.153437-0.412489-0.303783-0.325260-0.651742`.
- function_8: `0.100115-0.139025-0.121609-0.160743-0.802830-0.456884-0.232801-0.730775`; row 54. Best 9.99253623095 at `0.125164-0.146103-0.168096-0.157473-0.825605-0.491306-0.208638-0.710442`.

Policy review: Function 1 retains UCB 3.0 exploration because readings are essentially uninformative. Function 2 improved to 0.7499835443 but remains noisy; EI selects a nearby nonidentical validation point within 0.02, balancing potential improvement with local validation on the last round. Function 3 recovered from weak boundary probes, supporting EI within 0.15 of its incumbent. Function 4 declined for three queries; its generic trend classifier masks this behind an earlier best, so the final-round implementation now uses UCB 0.75 within 0.12 of the incumbent. Function 5's two inward probes lost yield; posterior mean stays within 0.02–0.10 of its corner, now excluding points within 0.005 of existing observations to prevent an effectively repeated query. Function 6 recovered somewhat but remains below its best; EI refinement stays within 0.08. Functions 7/8 returned slightly weaker latest outputs; UCB 0.35 within 0.20 retains refinement with modest uncertainty. High-dimensional data remain sparse. Predicted improvements for Functions 3/7/8 are uncertain, especially Function 3 (predicted -0.0046033 with standard deviation 0.0149).

Both optimiser copies received the policy corrections; intentional setup differences are preserved. Only Function 4/5 candidates changed from the first preview. Both optimisers and round helpers passed syntax verification. The append helper now ignores wholly empty trailing rows while retaining pending-input safeguards. Saved inputs, blank outputs, copied styles, all completed historical values, and exact repository workbook/budget snapshots were verified. Ledger charges round 13 once. No further evaluations may be prepared under this allocation.
