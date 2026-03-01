# Cache Eviction Policy Simulator

## Student Info
- Name: William Jesser
- UFID: 5963-4986

## How to Run
- Requires Python 3.10+.
- From the repo root: `python src/cache_sim.py <input-file>`
- Example: `python src/cache_sim.py data/example.in`
- Use `-` to read from stdin.
- Example (stdin, PowerShell here-doc):
  ```
  @"
  3 6
  1 2 3 1 2 4
  "@ | python src/cache_sim.py -
  ```

## Repository Layout
- `src/cache_sim.py` - simulator for FIFO, LRU, and OPTFF.
- `data/` - sample inputs (`*.in`) and expected outputs (`*.out`).
- `tests/` - unit tests (pytest).

## Example Input/Output
- Input: `data/example.in`
- Expected output (also in `data/example.out`):
```
FIFO : 4
LRU : 4
OPTFF : 4
```

## Written Component

### Q1. Empirical Comparison (>=50 requests each)
![alt text](image.png)

- OPTFF always has the fewest misses, making it the most optimal.
- FIFO vs LRU depends on the sequence. In file1/file3 LRU wins, but for file2, FIFO wins. This is beacuse in file2 FIFO beats LRU as the brusty repeats keep FIFOs queue stable, so LRU evicts useful items more often.

### Q2. Sequence where OPTFF < LRU (k = 3)
- Sequence: `1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5`
- Miss counts with k = 3: FIFO = 9, LRU = 10, OPTFF = 7.
- Why LRU loses: after `1,2,3`, the next `4` forces an eviction; LRU drops `1`. Soon after, `1` is needed twice before `3` or `4` return, so those misses cascade. OPTFF keeps items with the nearest future use (keeps `1,2,3`, evicts `4`), avoiding two misses.

### Q3. Proof sketch that OPTFF is optimal
Let OPT be Belady's farthest-in-future policy. Consider any offline algorithm A that knows the whole sequence. We transform A into OPT without adding misses.

Proof via Induction:
- Base Case: before the first request the caches are empty.
- Step: Assume that right before request I, OPT and A had the same cache. Proceed if both hit. Two situations arise if OPT evicts y (the page whose next usage is farthest in the future) and A misses and evicts some page x:
  1) A also evicts y; miss counts remain constant and caches remain aligned.
  2) A evicts x and keeps y: replace x with y. This swap cannot produce a new miss prior to y's subsequent use as y is used before any cached page. The updated algorithm now matches OPT at step i and has no more misses than A.

Repeating this transaction yields OPT with miss count <= any offline algorithm A. Thus, OPT is perfect for everyone.
We can produce OPT with miss count <= any offline algorithm A by repeating this transaction. OPT is therefore the best option for each sequence.

