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
        current_ice_cream (str): 現在コーンに積み上がっているアイス（文字列）
        current_pos (int): 現在の頂点番号
        prev_pos (int): 直前の頂点番号（Uターン禁止判定用）
        target_shop_index (int): 現在目指しているショップのインデックス (0 ~ K-1)
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
        # 今回の戦略では味変を行わないため、これらは固定値として扱う。
        self.tree_flavors: List[Optional[str]] = [None] * self.N
        for i in range(self.K, self.N):
            self.tree_flavors[i] = 'W'

        self.current_ice_cream = ""
        self.current_pos = 0
        self.prev_pos = -1 # 初回は移動元なし
        
        # 巡回戦略用のターゲット管理
        self.target_shop_index = 0

    def solve(self):
        """
        T回のステップを行い、行動を出力するメインループ。
        """
        for t in range(self.T):
            # --- 貪欲法: 行動決定ロジック ---
            
            # 今回は味変(行動2)を行わないため、移動(行動1)のみを考える。
            
            # 1. 現在のターゲットショップと目標の長さを決定
            target_shop = self.target_shop_index
            
            # ターゲットショップの現在の在庫を確認し、最大長を取得
            max_len_in_shop = 0
            for ice in self.shop_inventories[target_shop]:
                max_len_in_shop = max(max_len_in_shop, len(ice))
            
            # 目標: 「現在の最大長 + 1」の長さのアイスを作って持っていく
            required_len = max_len_in_shop + 1

            # 2. 条件を満たす移動先を探索 (BFS)
            next_move = self.get_next_move_for_target(target_shop, required_len)
            
            if next_move == -1:
                # もし条件を満たすパスが見つからない場合（長すぎるなど）
                # とりあえずターゲットショップに近づく単純な移動を行う（フォールバック）
                next_move = self.get_simple_move_to_target(target_shop)

            # 3. 移動処理の実行と状態更新
            self.execute_move(next_move)
            
            # 出力
            print(f"{next_move}")
            sys.stdout.flush()

            # 4. ターゲット更新判定
            # 移動後、ターゲットショップに到着していたら（納品完了）、次のショップへターゲットを切り替える
            if self.current_pos == target_shop:
                # 次のショップへ (0 -> 1 -> ... -> K-1 -> 0)
                self.target_shop_index = (self.target_shop_index + 1) % self.K

    def get_next_move_for_target(self, target_shop: int, required_len: int) -> int:
        """
        ターゲットショップに向かうルートの中で、
        「到着時のアイスの長さ >= required_len」を満たす最短ルートの『最初の一手』を返す。
        
        制約:
        - 直前の頂点には戻れない (Uターン禁止)
        - ターゲット以外のショップを通ってはいけない（強制納品されてリセットされるため）
        
        Returns:
            int: 次の移動先頂点ID。見つからない場合は -1。
        """
        start_node = self.current_pos
        start_len = len(self.current_ice_cream)
        prev_node = self.prev_pos

        # BFS Queue: (current_node, previous_node, current_ice_length, first_move_direction)
        queue = deque()

        # --- 初手の展開 ---
        # ここで初手を決め打ちしてキューに入れることで、ゴールしたときに「どっちの方向に進めばいいか」がわかる
        for neighbor in self.adj[start_node]:
            if neighbor == prev_node:
                continue
            
            # 次の状態を計算
            next_len = start_len
            if self.is_tree(neighbor):
                next_len += 1
            elif self.is_shop(neighbor):
                # ショップの場合、長さは増えない
                # かつ、それがターゲットでないなら、このルートは不可（リセットされるため）
                if neighbor != target_shop:
                    continue
            
            # いきなりゴールに到達した場合
            if neighbor == target_shop:
                if next_len >= required_len:
                    return neighbor
                else:
                    # 長さが足りないままゴールしてしまう -> この方向はダメ（通過できないので詰み）
                    continue

            # キューに追加
            queue.append((neighbor, start_node, next_len, neighbor))

        # 訪問済み管理: (node, ice_len) を保持
        # ※ 厳密には (node, prev_node, ice_len) だが、計算量削減のため簡易化
        # 同じ場所に同じ長さで到達したら、後から来た方は遅いので不要
        visited = set() 
        for q in queue:
            visited.add((q[0], q[2]))

        # 探索ステップ制限（計算時間オーバー防止）
        steps = 0
        MAX_STEPS = 2000

        while queue:
            curr, prev, length, first_move = queue.popleft()
            steps += 1
            if steps > MAX_STEPS:
                break
            
            # 枝刈り: 必要長さより明らかに長くなりすぎたら打ち切る (+3程度余裕を見る)
            if length > required_len + 3:
                continue

            for neighbor in self.adj[curr]:
                if neighbor == prev:
                    continue # Uターン禁止

                # 次の状態
                new_len = length
                if self.is_tree(neighbor):
                    new_len += 1
                elif self.is_shop(neighbor):
                    # ショップ到達時の処理
                    if neighbor != target_shop:
                        # ターゲット以外のショップは通過禁止
                        continue
                
                # ゴール判定
                if neighbor == target_shop:
                    if new_len >= required_len:
                        return first_move
                    else:
                        # 長さが足りないままゴール -> 通過できないのでこのルートは終了
                        continue
                
                # 訪問済みチェックと追加
                state = (neighbor, new_len)
                if state not in visited:
                    visited.add(state)
                    queue.append((neighbor, curr, new_len, first_move))
        
        return -1

    def get_simple_move_to_target(self, target_shop: int) -> int:
        """
        条件を満たすパスが見つからなかった場合のフォールバック。
        長さ条件を無視して、単純にターゲットショップへ最短で向かうルートの初手を返す。
        ただし、他のショップは避ける。
        """
        queue = deque([(self.current_pos, self.prev_pos, -1)]) # (curr, prev, first_move)
        visited = {self.current_pos}
        
        candidates = []

        # 初手
        for neighbor in self.adj[self.current_pos]:
            if neighbor == self.prev_pos: continue
            if self.is_shop(neighbor) and neighbor != target_shop: continue
            
            if neighbor == target_shop:
                return neighbor
            
            queue.append((neighbor, self.current_pos, neighbor))
            visited.add(neighbor)

        while queue:
            curr, prev, first_move = queue.popleft()
            
            for neighbor in self.adj[curr]:
                if neighbor == prev: continue
                if self.is_shop(neighbor) and neighbor != target_shop: continue
                
                if neighbor == target_shop:
                    return first_move
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, curr, first_move))
        
        # どうしても行けない場合（ほぼあり得ないが）、ランダムに動く
        for neighbor in self.adj[self.current_pos]:
            if neighbor != self.prev_pos:
                return neighbor
        return self.adj[self.current_pos][0]

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
        else:
            # ショップの場合: 納品
            if self.current_ice_cream not in self.shop_inventories[v]:
                self.shop_inventories[v].add(self.current_ice_cream)
            
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