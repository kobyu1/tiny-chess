# tiny-chess

A chess engine in 4 KB of Python, built for the make.fun
[tiny-chess-01](https://make.fun/c/tiny-chess-01) bounty
("Build the strongest chess engine in 4 KB of Python").

`main.py` is a self-contained program (Python 3.13, standard library
only): an original negamax alpha-beta engine with a transposition
table, quiescence search, late-move reductions and piece-square-table
evaluation, packed with lzma into a single file under 4,096 bytes.
It plays the house gauntlet over the `MAKEFUN_ENV_URL` HTTP API.

Validation before submission:

- Perft: the move generator reproduces the known node counts for all
  six standard test positions exactly (the packed payload was
  re-verified, not just the readable source).
- Local practice trials (6 games each, 60k node budget): trial-0
  scored 4.0 points (Elo ≈ 1,451) and trial-1 scored 2.5 points,
  against a house floor of 1,154 and a house-baseline practice
  average of ≈ 1,365.
- Time safety: the slowest single move took ≈ 3.3 s of the 10 s
  limit; the engine's own thinking time was 16–29 s per 6-game
  trial, far inside the 1,800 s match budget.

Run it with the environment URL set:

    MAKEFUN_ENV_URL=http://127.0.0.1:PORT python3 -P -s main.py

MIT licensed.
