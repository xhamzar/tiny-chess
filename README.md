# tiny-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/xhamzar/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/xhamzar/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A 4 KB chess engine for the make.fun `tiny-chess-01` bounty — see the
[bounty page](https://make.fun/bounty/tiny-chess-01). One file,
`main.py` (4,074 bytes), Python 3.13 standard library only, no other files
read at runtime.

## Design

- **Board:** 0x88 (a 128-cell list), integer pieces, sign for colour.
- **Search:** negamax + alpha-beta, iterative deepening with a **fixed node
  budget** (80,000 nodes — no clock, so replays are move-for-move
  identical), quiescence (captures only, 50-ply cap), **null-move pruning**
  (reduction 2, skipped when in check).
- **Transposition table:** exact/lower/upper flags, keyed on
  `(board, side, castling, en-passant)`; reset every move, as is the killer
  table, so each move depends only on the position.
- **Move ordering:** table move, killer move (one per ply), then captures by
  victim value.
- **Evaluation:** material + procedural piece-square tables (centralisation
  and advancement). Mate scores prefer faster mates (spare plies).
- **Protocol:** talks to the env over HTTP (`$MAKEFUN_ENV_URL`):
  `POST /game`, `POST /move` (UCI). Any search error falls back to the first
  legal move, so it never crashes a game.

## Verified locally

- Perft correct on 6 standard positions (start, kiwipete, pos3–pos6) to
  depth 3–4, including castling, en passant and promotions.
- Finds mate in 1, takes a hanging queen, deterministic (same position twice
  gives the same move and node count).
- ~30k nodes/second on one CPU; 80k nodes ≈ 2.5–3 s/move; reaches depth 5 in
  the opening, depth 4 in the middlegame at that budget.

## Licence

MIT — see `LICENSE`.
