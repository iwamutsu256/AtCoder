import sys
import random
import time

# グローバル定数
N = 36       # 好きな文字列の数
M = 12       # 状態数
L = 10**6    # 生成する文字列の長さ

def debug(*args, **kwargs):
    """
    デバッグ用に標準エラー出力 (stderr) にメッセージを出力する。
    通常の print() と同様に使える。
    """
    print(*args, file=sys.stderr, **kwargs)



import math
from typing import List, Tuple

def compute_score(
    S: List[str], P: List[int], L: int, C: List[str], A: List[List[int]]
) -> int:
    """
    与えられたモデル(C, A)と文字列リストS, スコアP, 長さLに基づいてスコアを計算する。
    S[i] が L 長の出力に1回でも出現する確率を Q_i として、 sum(P_i * Q_i) を返す。
    """
    total_score = 0.0
    for s, p in zip(S, P):
        prob = compute_word_probability(s, L, C, A)
        total_score += p * prob
    return round(total_score)

def compute_word_probability(
    word: str, L: int, C: List[str], A: List[List[int]]
) -> float:
    """
    文字列 `word` が長さLの生成文字列に少なくとも1回現れる確率を返す。
    """
    M = len(C)
    states = {}
    n = 0

    for j in range(M):
        states[(0, j)] = n
        n += 1
        for i in range(len(word) - 1):
            if word[i] == C[j]:
                states[(i + 1, j)] = n
                n += 1

    X = [0.0] * (n * n)
    for (length, u), j in states.items():
        for v in range(M):
            next_seq = word[:length] + C[v]
            s = 0
            while s < len(next_seq) and next_seq[s:] != word[:len(next_seq) - s]:
                s += 1
            if len(next_seq) - s != len(word):
                next_state = states.get((len(next_seq) - s, v))
                if next_state is not None:
                    X[next_state * n + j] += A[u][v] / 100.0

    Y = [1.0 if i == j else 0.0 for i in range(n) for j in range(n)]
    power = L - 1
    while power > 0:
        if power & 1:
            Y = matmul(Y, X, n)
        X = matmul(X, X, n)
        power >>= 1

    init_state = states[(1, 0)] if C[0] == word[0] else states[(0, 0)]
    prob_not_occur = sum(Y[i * n + init_state] for i in range(n))
    return max(0.0, min(1.0, 1.0 - prob_not_occur))

def matmul(a: List[float], b: List[float], n: int) -> List[float]:
    """
    n×n行列 a と b の積を返す（行優先1次元表現）。
    """
    c = [0.0] * (n * n)
    for i in range(n):
        for k in range(n):
            for j in range(n):
                c[i * n + j] += a[i * n + k] * b[k * n + j]
    return c

strings = []
def construct_model():
    limit = 1.8
    start = time.time()
    ret_seqs = []
    best = 0
    for step in range(10000):
        if time.time()-start > limit:
            break
        n = [3,4,5,6,7][step%5]
        seqs, sc = find_solution(num_of_accept = n, time_limit = limit - (time.time() - start))
        debug(f"{n=}, {sc=}, {time.time() - start=}")
        model = construct_model_from_seqs(seqs)
        score = compute_score(S = [s for _, s in strings[:n]], P = [p for p, _ in strings[:n]], L = L, C = model[0], A = model[1])
        debug(f"{step=}, {score=}")
        if score > best:
            best = score
            best_model = model
    return best_model

def construct_model_from_seqs(seqs):
    graph = [[] for _ in range(M)]
    for seq in seqs:
        for j1,j2 in zip(seq[:-1], seq[1:]):
            if j2 not in graph[j1]:
                graph[j1].append(j2)
    transitions = []
    for i in range(M):
        trans = [0] * M
        while sum(trans) < 100:
            if len(graph[i]) == 0:
                for j in range(M):
                    if sum(trans) < 100:
                        trans[j] += 1
            for j in graph[i]:
                if sum(trans) < 100:
                    trans[j] += 1
        transitions.append(trans)
    return "abcdefabcdef", transitions

def find_solution(num_of_accept, time_limit):
    characters = "abcdefabcdef"
    start = time.time()
    def get_random_seqs():
        seqs = []
        for word in range(num_of_accept):
            string = strings[word][1]
            seq = []
            for c in string:
                inds = [i for i, x in enumerate(characters) if x == c]
                ind = random.choice(inds)
                seq.append(ind)
            seqs.append(seq)
        return seqs
    def get_score(seqs):
        graph = [[] for _ in range(M)]
        for seq in seqs:
            for j1, j2 in zip(seq[:-1], seq[1:]):
                if j2 not in graph[j1]:
                    graph[j1].append(j2)
        us = []
        for seq in seqs:
            v = 1
            for j1, j2 in zip(seq[:-1], seq[1:]):
                v *= len(graph[j1])
            us.append(v)
        return max(us)
    
    seqs = get_random_seqs()
    best = get_score(seqs)

    cnt = 0
    while time.time() - start < time_limit:
        cnt += 1
        if cnt > 200:
            break
        word = random.randint(0, num_of_accept - 1)
        j = random.randint(0, len(seqs[word]) - 1)
        c = strings[word][1][j]
        inds = [i for i, x in enumerate(characters) if x == c]
        ind = random.choice(inds)
        if ind == seqs[word][j]:
            continue
        old_ind = seqs[word][j]
        seqs[word][j] = ind
        score = get_score(seqs)
        if score <= best:
            if score < best:
                cnt = 0

            best = score
        else:
            seqs[word][j] = old_ind
    return seqs, best

def output_model(characters, transitions):
    """モデルの出力"""
    for i in range(M):
        row = [str(transitions[i][j]) for j in range(M)]
        print(f"{characters[i]} {' '.join(row)}")

def main():
    input_data = sys.stdin.read().splitlines()
    global N, M, L
    N, M, L = map(int, input_data[0].split())
    for line in input_data[1:]:
        s, p = line.split()
        strings.append((int(p), s))
    strings.sort(reverse=True)

    characters, transitions = construct_model()
    output_model(characters, transitions)

if __name__ == "__main__":
    main()
