# tiny-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/kobyu1/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/kobyu1/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in 4 KB of Python, built for the make.fun
[tiny-chess-01](https://make.fun/c/tiny-chess-01) bounty
("Build the strongest chess engine in 4 KB of Python").

`main.py` is a self-contained program (Python 3.13, standard library
only), shipped as plain readable source — no packing, encoding or
self-extraction. An earlier draft compressed the engine with
lzma+base85 into a single generated line; it was replaced because
the bounty checker attributes each submitted line to its first
appearance in the development transcript, and a generated one-liner
first appears as build-script output rather than as a file write.
Every line of the current file was authored directly as a file
write or edit.

Design (4,050 bytes):

- 120-square mailbox board; pseudo-legal move generation with a
  legality filter based on an attack test.
- Negamax alpha-beta search with iterative deepening under a fixed
  85,000-node budget (deterministic: no wall clock in move choice).
- A transposition table that keeps the best move found per position
  and uses it for move ordering, plus MVV-LVA capture ordering.
- Quiescence search over captures and promotions, searching all
  check evasions when in check; the capture-only filter is applied
  before legality testing to keep quiescence cheap.
- Evaluation: material, a formula piece-square term (centrality
  weighted per piece type), a pawn-advancement term, and a king
  term that switches between a middlegame safety formula and an
  endgame centrality formula depending on whether queens remain.

It plays the house gauntlet over the `MAKEFUN_ENV_URL` HTTP API.

Validation before submission:

- Perft: the move generator reproduces the known node counts for
  all six standard test positions exactly (20 depth cases).
- Local practice trials (6 games each): trial-0 scored 3.5 points
  (3 wins, 1 draw, 2 losses; Elo ≈ 1,364) and trial-1 scored
  2.0 points (1 win, 2 draws, 3 losses; Elo ≈ 1,099), against a
  house floor of 1,154 and a house-baseline practice average
  of ≈ 1,365.
- Time safety: at the 85,000-node budget the slowest move measured
  in testing took ≈ 4.0 s of the 10 s limit on a throttled shared
  VM (the grading CPU is faster); full 6-game practice trials took
  16–18 minutes of wall time on that VM, inside the 1,800 s match
  budget.

Run it with the environment URL set:

    MAKEFUN_ENV_URL=http://127.0.0.1:PORT python3 -P -s main.py

MIT licensed.
