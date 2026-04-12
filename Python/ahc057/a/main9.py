import sys
import math
import heapq
import random

# --- 幾何計算関数 ---

def calc_torus_dist_sq(x1, y1, x2, y2, L):
    """
    トーラス環境下での2点間の距離の二乗を計算する。
    """
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    dist_x = min(dx, L - dx)
    dist_y = min(dy, L - dy)
    return dist_x**2 + dist_y**2

# --- Union-Find (クラスカル法用) ---

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            return True
        return False

# --- メインソルバー ---

def solve():
    # 入力
    input = sys.stdin.readline
    try:
        line1 = input().split()
        if not line1: return
        N, T, M, K, L = map(int, line1)
    except ValueError:
        return

    # 原子情報の読み込みと、最終位置の事前計算
    atoms = []
    last_t = T - 1
    
    for i in range(N):
        x, y, vx, vy = map(int, input().split())
        
        # 最終ターン (T-1) における位置を計算
        # 途中で結合しなければ等速直線運動をするため、これで確定できる
        fx = (x + vx * last_t) % L
        fy = (y + vy * last_t) % L
        
        atoms.append({
            'id': i, 
            'x': x, 'y': y, 
            'vx': vx, 'vy': vy,
            'fx': fx, 'fy': fy
        })

    all_operations = []
    used = [False] * N
    random.seed(42)
    
    # --- 逐次構築ループ ---
    # M個のグループを1つずつ順番に作成する
    for _ in range(M):
        # 1. 核(Seed)の選択
        # 未使用の原子からランダムに選ぶ
        available_indices = [i for i in range(N) if not used[i]]
        if not available_indices: break
        
        seed_idx = random.choice(available_indices)
        seed_atom = atoms[seed_idx]
        
        # 2. メンバー選抜 (Clustering Phase)
        # 最終位置(T-1)における距離がSeedに近い順にK個(自分含む)を選ぶ
        candidates = []
        for idx in available_indices:
            atom = atoms[idx]
            d2 = calc_torus_dist_sq(seed_atom['fx'], seed_atom['fy'], atom['fx'], atom['fy'], L)
            candidates.append((d2, idx))
        
        candidates.sort(key=lambda x: x[0])
        
        # 上位K個を取得
        cluster_indices = [x[1] for x in candidates[:K]]
        
        # 使用済みフラグ更新
        for idx in cluster_indices:
            used[idx] = True
            
        # 3. MST (最小全域木) の構築
        # 選ばれた30個の原子について、最終位置での距離をコストとした完全グラフを作り、
        # クラスカル法でMSTを構築する。
        
        edges = []
        n_cluster = len(cluster_indices)
        
        # クラスター内の全ペアについて距離計算
        for i in range(n_cluster):
            u = cluster_indices[i]
            for j in range(i + 1, n_cluster):
                v = cluster_indices[j]
                d2 = calc_torus_dist_sq(atoms[u]['fx'], atoms[u]['fy'], atoms[v]['fx'], atoms[v]['fy'], L)
                edges.append((d2, u, v))
        
        # コスト順にソート
        edges.sort(key=lambda x: x[0])
        
        # クラスカル法実行
        # UnionFindは全原子数Nで初期化しておけばID変換不要
        uf = UnionFind(N)
        mst_edges = []
        
        for d2, u, v in edges:
            if uf.union(u, v):
                mst_edges.append((u, v))
                # 辺の数が頂点数-1になれば終了
                if len(mst_edges) == n_cluster - 1:
                    break
        
        # 4. 操作出力
        # MSTの辺を結合操作として追加。時刻はすべて T-1。
        # 問題文の仕様上、同一時刻に複数の結合を出力しても、順次処理され1つの成分にまとまる。
        # (MSTのエッジには閉路がないため、どの順番で結合しても矛盾なく連結される)
        for u, v in mst_edges:
            all_operations.append(f"{last_t} {u} {v}")

    # 結果出力
    for op in all_operations:
        print(op)

if __name__ == "__main__":
    solve()