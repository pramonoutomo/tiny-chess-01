# tiny-chess-01 entry

A 0x88 chess engine packed into a main.py under 4,096 bytes.

- Principal-variation search with a transposition table, null-move pruning,
  late-move reduction, killers and quiescence.
- Tapered material + piece-square evaluation with pawn, rook-file and bishop-pair
  terms.
- Node-budgeted, never clocked: same position, same move.

`main.py` is the whole engine: an lzma payload of `src/engine.py` and the stub
that unpacks it. Python 3.13 standard library only; it reads no other file.
