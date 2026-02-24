import argparse
from collections import deque, OrderedDict, defaultdict
import sys

def parse_input(path: str):
    with (open(path, "r") if path != "-" else sys.stdin) as f:
        tokens = [int(tok) for tok in f.read().split()]
    if len(tokens) < 2:
        raise ValueError("Input must start with: k m")
    k, m = tokens[0], tokens[1]
    if k < 1:
        raise ValueError("Cache capacity k must be at least 1")
    requests = tokens[2:]
    if m != len(requests):
        raise ValueError(f"Expected {m} requests but found {len(requests)}")
    return k, requests

def simulate_fifo(k: int, requests):
    cache = set()
    order = deque()
    misses = 0
    for r in requests:
        if r in cache:
            continue
        misses += 1
        if len(cache) == k:
            victim = order.popleft()
            cache.remove(victim)
        cache.add(r)
        order.append(r)
    return misses

def simulate_lru(k: int, requests):
    cache = OrderedDict()
    misses = 0
    for r in requests:
        if r in cache:
            cache.move_to_end(r)
            continue
        misses += 1
        if len(cache) == k:
            cache.popitem(last=False)
        cache[r] = None
    return misses

def simulate_optff(k: int, requests):
    future_positions = defaultdict(list)
    for idx, val in enumerate(requests):
        future_positions[val].append(idx)
    # convert lists to deques for O(1) pops from left
    for val in future_positions:
        future_positions[val] = deque(future_positions[val])

    cache = set()
    misses = 0

    for idx, r in enumerate(requests):
        future_positions[r].popleft()  # drop current occurrence

        if r in cache:
            continue
        misses += 1
        if len(cache) < k:
            cache.add(r)
            continue
        # choose victim with farthest next use (or never used again)
        farthest_item = None
        farthest_next = -1
        for item in cache:
            nxt = future_positions[item][0] if future_positions[item] else float("inf")
            if nxt > farthest_next:
                farthest_next = nxt
                farthest_item = item
        cache.remove(farthest_item)
        cache.add(r)

    return misses

def main(argv=None):
    parser = argparse.ArgumentParser(description="Cache eviction policy simulator")
    parser.add_argument("input", help="Input file path or '-' for stdin")
    args = parser.parse_args(argv)

    k, requests = parse_input(args.input)
    fifo = simulate_fifo(k, requests)
    lru = simulate_lru(k, requests)
    opt = simulate_optff(k, requests)

    print(f"FIFO : {fifo}")
    print(f"LRU : {lru}")
    print(f"OPTFF : {opt}")

if __name__ == "__main__":
    main()


