import sys
import math
import random
from collections import deque
from typing import List, Set, Dict, Tuple, Optional

# ------------------------------------------------------------------------------
# クラス・関数定義
# ------------------------------------------------------------------------------

class IceCreamSolver:
    """
    AHC 'Ice Cream Collection' 問題を解くためのソルバークラス。
    
    Attributes:
        N (int): 頂点数
        M (int): 辺数
        K (int): アイスクリームショップの数 (頂点 0 ~ K-1)
        T (int): 最大行動回数
        adj (List[List[int]]): 隣接リスト
        shop_inventories (List[Set[str]]): 各ショップの在庫集合（納品済みの文字列）
        tree_flavors (List[str]): 各木のアイスの味 ('W' or 'R')。ショップの場合は空文字など。
        target_flavors (List[str]): 戦略的にその木をどちらの味にしたいか ('W' or 'R')
        current_ice_cream (str): 現在コーンに積み上がっているアイス（文字列）
        current_pos (int): 現在の頂点番号
        prev_pos (int): 直前の頂点番号（Uターン禁止判定用）
    """

    def __init__(self):
        """
        標準入力から問題を読み込み、初期状態を設定する。
        input() を使用して、対話的な入力や貼り付けに対応。
        """
        try:
            # 1行目: N, M, K, T
            line1 = input().split()
            if not line1: return
            self.N, self.M, self.K, self.T = map(int, line1)

            # グラフ構築 (M行)
            self.adj = [[] for _ in range(self.N)]
            for _ in range(self.M):
                line = input().split()
                u, v = int(line[0]), int(line[1])
                self.adj[u].append(v)
                self.adj[v].append(u)

            # 座標読み込み (N行)
            self.coords = []
            for _ in range(self.N):
                line = input().split()
                x, y = int(line[0]), int(line[1])
                self.coords.append((x, y))

        except (EOFError, ValueError):
            # 入力が途中で切れた場合などのエラー処理
            sys.stderr.write("入力の読み込み中にエラーが発生しました。\n")
            return

        # --- 状態の初期化 ---
        self.shop_inventories: List[Set[str]] = [set() for _ in range(self.K)]
        
        # 頂点 K ~ N-1 は木。初期状態は全て 'W'。0 ~ K-1 はショップなので None 扱い。
        self.tree_flavors: List[Optional[str]] = [None] * self.N
        for i in range(self.K, self.N):
            self.tree_flavors[i] = 'W'

        # 戦略: ランダムに約半分の木を 'R' に変えることを目指す
        # これにより生成できる文字列の多様性を増やす
        self.target_flavors: List[Optional[str]] = [None] * self.N
        random.seed(42) # 再現性のためシード固定
        for i in range(self.K, self.N):
            self.target_flavors[i] = 'R' if random.random() < 0.5 else 'W'

        self.current_ice_cream = ""
        self.current_pos = 0
        self.prev_pos = -1 # 初回は移動元なし

    def solve(self):
        """
        T回のステップを行い、行動を出力するメインループ。
        """
        for t in range(self.T):
            # --- 貪欲法: 行動決定ロジック ---
            
            # 1. 味変チェック (Action 2)
            # 現在地が木であり、現在の味が 'W' で、かつ戦略的に 'R' にしたい場合
            if self.is_tree(self.current_pos):
                if (self.tree_flavors[self.current_pos] == 'W' and 
                    self.target_flavors[self.current_pos] == 'R'):
                    
                    # 行動2を実行
                    print("-1") # Action 2 output
                    self.tree_flavors[self.current_pos] = 'R'
                    # Action 2 は移動しないので、prev_pos は更新しない（ルール上移動扱いではない）
                    # ただし、問題文の「2回目以降の行動1では...」の制約には影響しない
                    sys.stdout.flush()
                    continue

            # 2. 移動先決定 (Action 1)
            best_next_node = self.decide_next_move()
            
            # 移動処理の実行と状態更新
            self.execute_move(best_next_node)
            
            # 出力
            print(f"{best_next_node}")
            sys.stdout.flush()

    def decide_next_move(self) -> int:
        """
        現在地から移動可能な隣接頂点のうち、
        「最も近い有効なショップ（新しい文字列を納品できる店）」への経路となりうる
        最適な頂点を決定する。

        Returns:
            int: 次に移動すべき頂点番号
        """
        candidates = []
        for v in self.adj[self.current_pos]:
            if v == self.prev_pos:
                continue # Uターン禁止
            candidates.append(v)

        if not candidates:
            # 万が一行き止まり（2-辺連結なので無いはずだが念のため）
            # Uターンせざるを得ない場合のフォールバック
            return self.adj[self.current_pos][0]

        best_v = -1
        min_dist_to_reward = float('inf')

        # 各候補について、「そこに進んだ場合、最短何手で有効な納品ができるか」を評価
        for v in candidates:
            dist = self.bfs_distance_to_nearest_valid_shop(v, self.current_pos)
            
            # より近いステップで納品できるルートを優先
            # 同点の場合はランダム性を持たせるか、インデックス順（ここでは単純比較）
            if dist < min_dist_to_reward:
                min_dist_to_reward = dist
                best_v = v
            elif dist == min_dist_to_reward:
                # 距離が同じなら、ランダムに選ぶことでループを回避する確率を上げる
                if random.random() < 0.5:
                    best_v = v

        return best_v

    def bfs_distance_to_nearest_valid_shop(self, start_node: int, forbidden_prev: int) -> int:
        """
        start_node から開始して、有効な（まだ持っていない文字列を受け取る）ショップまでの
        最短距離をBFSで計算する。

        Args:
            start_node (int): 探索開始頂点（次の移動先候補）
            forbidden_prev (int): start_node に来る前の頂点（Uターン禁止対応用）

        Returns:
            int: 最短距離。見つからない場合は無限大。
        """
        # (現在頂点, 距離) のキュー
        # 注意: 厳密なシミュレーションには「手持ちのアイス」の変化も必要だが、
        # 計算量削減のため「現在の文字列 + start_nodeで得られる文字」をベースに、
        # 「その後はどんな文字がつこうが、とにかく最短でショップにつけばOK」
        # という緩い条件で探索する（これを厳密にやると状態爆発する）。
        
        # 予測されるアイス文字列（start_nodeに進んだ時点での状態）
        predicted_ice = self.current_ice_cream
        if self.is_tree(start_node):
            # まだ味変していない可能性も考慮すべきだが、現状の flavor を使う
            predicted_ice += self.tree_flavors[start_node]
        
        # --- BFS 初期化 ---
        # visited は (頂点) だけで管理する（簡易版）
        # ※ 厳密には (頂点, 来た方向) だが、距離計測目的なので頂点単位で枝刈り
        queue = deque([(start_node, 0)])
        visited = {start_node}
        
        # スタート直後のUターン禁止用フラグ（BFSの1歩目だけ親に戻れない）
        # ただし、グラフ全体の探索において、この関数は「start_nodeから先」を見るので、
        # start_node の親である forbidden_prev には戻らないようにする。
        # 実際には visited に forbidden_prev を入れれば解決。
        visited.add(forbidden_prev)

        while queue:
            curr, dist = queue.popleft()

            # 探索打ち切り（あまり遠すぎると計算の無駄＆信頼性が低い）
            if dist > 15: 
                return float('inf')

            # --- 判定: ここがショップなら納品可能か？ ---
            if self.is_shop(curr):
                # ここで納品した場合、新しい文字列になるか？
                # 注意: BFS探索中の経路上の追加文字は無視し、
                # 「とりあえずここまで来たら納品する」と仮定して判定する（軽量化）
                # 精度を上げるなら経路上の文字も足すべきだが、Greedyではこれで十分なことが多い。
                if predicted_ice not in self.shop_inventories[curr]:
                    return dist

            # --- 次の探索 ---
            for neighbor in self.adj[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return float('inf')

    def execute_move(self, v: int):
        """
        頂点 v への移動を確定し、内部状態（現在地、アイス、在庫）を更新する。

        Args:
            v (int): 移動先頂点
        """
        # Uターン禁止制約のための更新
        self.prev_pos = self.current_pos
        self.current_pos = v

        if self.is_tree(v):
            # 木の場合: アイスを収穫
            flavor = self.tree_flavors[v]
            self.current_ice_cream += flavor
            # 文字列長が爆発しないように制限をかける戦略もありうるが、
            # まずは制限なしで実装する。
        else:
            # ショップの場合: 納品
            # まだ登録されていないなら登録
            if self.current_ice_cream not in self.shop_inventories[v]:
                self.shop_inventories[v].add(self.current_ice_cream)
            else:
                # 既に登録済みでも、空文字 ("") を登録したことになるので
                # 問題文的には「変化しない」だけ。
                pass
            
            # コーンを空にする
            self.current_ice_cream = ""

    def is_tree(self, v: int) -> bool:
        """頂点 v が木かどうか判定"""
        return v >= self.K

    def is_shop(self, v: int) -> bool:
        """頂点 v がショップかどうか判定"""
        return v < self.K

# ------------------------------------------------------------------------------
# メイン実行部
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    solver = IceCreamSolver()
    solver.solve()