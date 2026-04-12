import sys
import numpy as np
from scipy.optimize import minimize
from itertools import combinations

def read_input():
    n, m = map(int, sys.stdin.readline().split())
    tubes = [tuple(map(float, sys.stdin.readline().split())) for _ in range(n)]
    targets = [tuple(map(float, sys.stdin.readline().split())) for _ in range(m)]
    return tubes, targets

def color_distance(c1, c2):
    return np.linalg.norm(np.array(c1) - np.array(c2))

def mix_colors(c1, c2, w):
    return w * np.array(c1) + (1 - w) * np.array(c2)

def best_mix(target, tubes):
    best_err = float('inf')
    best_combo = None
    for i, j in combinations(range(len(tubes)), 2):
        def err(w):
            mixed = mix_colors(tubes[i], tubes[j], w[0])
            return color_distance(mixed, target)
        res = minimize(err, [0.5], bounds=[(0, 1)])
        if res.fun < best_err:
            best_err = res.fun
            best_combo = (i, j, res.x[0])
    return best_combo, best_err

def solve(tubes, targets, epsilon=0.05):
    for target in targets:
        combo, err = best_mix(target, tubes)
        if err < epsilon:
            i, j, w = combo
            print(f"mix {i} {j} {w:.6f}")
        else:
            i = min(range(len(tubes)), key=lambda k: color_distance(tubes[k], target))
            print(f"single {i}")

if __name__ == "__main__":
    tubes, targets = read_input()
    solve(tubes, targets)
