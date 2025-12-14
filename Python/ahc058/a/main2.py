import sys
from typing import List, Tuple, Optional

# --- クラス定義: 問題の定数や入力を管理 ---
class ProblemInput:
    """
    問題の入力データと定数を管理するクラスです。
    """
    def __init__(self):
        # 1行目の入力: N, L, T, K
        self.N, self.L, self.T, self.K = map(int, sys.stdin.readline().split())

        # 2行目の入力: Level 0 の機械の生産能力 A
        self.A = list(map(int, sys.stdin.readline().split()))

        # 続くL行: 各Levelの機械の初期コスト C
        self.C = []
        for _ in range(self.L):
            self.C.append(list(map(int, sys.stdin.readline().split())))

# --- クラス定義: 投資価値計算機 ---
class InvestmentAnalyzer:
    """
    各レベルの機械を強化した際の効果（Gain）を計算するためのクラスです。
    """
    def __init__(self, input_data: ProblemInput):
        self.input_data = input_data
        # weights[i][t] = Level i の機械のパワーを、残りターン数 t の時点で 1 上げたとき、
        #                 最終的に「Level 0の機械が累計で何回稼働した分」に相当するかを保持するテーブル。
        #                 これに A[j] を掛ければ、実際のりんごの増加数になる。
        self.weights = self._precompute_weights()

    def _precompute_weights(self) -> List[List[int]]:
        """
        動的計画法(DP)により、各レベル・残りターン数ごとの重みを事前計算します。
        """
        L = self.input_data.L
        T = self.input_data.T
        
        # weights[lvl][remaining_turns]
        W = [[0] * (T + 1) for _ in range(L)]

        # DPで埋める
        # remaining_turns が 0 のときは何も生産しないので 0 のまま
        for t in range(1, T + 1):
            # Level 0: 残りターン数 t 回分だけ稼働する
            # (ターン t で強化 -> そのターンから生産開始 -> 残り t 回生産)
            W[0][t] = t
            
            # Level 1以上: 
            # Level i を強化すると、毎ターン Level i-1 の機械が増える。
            # 残りターン t のとき、
            #  1. このターンに Level i-1 が増える（のか？）
            #     問題文の順序: Level 0処理 -> Level 1処理(Level 0が増える) ...
            #     つまり、ターン t で Level i (i>=1) を強化しても、
            #     その効果で Level i-1 が増えるのは計算順序的に「Level i-1 の処理が終わった後」かもしれないし、
            #     あるいは即時反映かもしれない。
            #     
            #     厳密な順序:
            #     Action(強化) -> Level 0 Prod -> Level 1 Prod (B0増) -> Level 2 Prod (B1増)...
            #
            #     例: ターン t で Level 1 (i=1) を強化 (P1 += 1)
            #     -> Level 0 Prod (影響なし)
            #     -> Level 1 Prod (B0 += P1)  <-- ここで B0 が増える！
            #     
            #     つまり、このターン(t)の生産フェーズで B0 が増えるが、
            #     B0 がりんごを作るのは「Level 0 Prod」のフェーズ。
            #     Level 0 Prod は Level 1 Prod より「先」に行われるため、
            #     増えた B0 がりんごを作り始めるのは「次のターン (t-1)」からとなる。
            #
            #     よって、Level i (i>=1) の残りターン t での価値は、
            #     Level i-1 の残りターン t-1, t-2, ..., 1 での価値の総和になる。
            
            for i in range(1, L):
                # W[i][t] = W[i][t-1] (昨までの累積) + W[i-1][t] (今増えた分が将来生む価値) ?
                # いや、上記の考察により「1ターン遅れる」。
                # Level i のパワーがある状態で1ターン過ごすと、Level i-1 が 1個増える。
                # その増えた 1個 は、残りターン t-1 の状態で存在する。
                # よって、 W[i][t] = W[i][t-1] (パワーはそのままだから継続) + W[i-1][t-1] (新しく生まれた子の価値)
                # ※厳密には P は減らないので、累積していくイメージ。
                
                # 漸化式: W[i][t] = W[i][t-1] + W[i-1][t-1] (i >= 1 の場合、効果発揮は次ターンからなので t-1 を参照)
                # Level 0 は即時反映なので W[0][t] = t だったが、
                # Level 1 は 次のターンから Level 0 として働くので。
                W[i][t] = W[i][t-1] + W[i-1][t-1]

        return W

    def get_gain(self, i: int, j: int, current_turn: int) -> int:
        """
        現在ターンにおいて、機械(i, j)を強化した場合の
        最終的なりんご増加数(Gain)を計算して返します。
        
        Args:
            i: Level
            j: ID
            current_turn: 現在のターン番号 (0-indexed)
            
        Returns:
            int: 予想されるりんご増加総数
        """
        remaining_turns = self.input_data.T - current_turn
        
        # 残りターンがないなら価値は0
        if remaining_turns <= 0:
            return 0
            
        # 基本的な重み（A[j]を含まない係数）
        base_weight = self.weights[i][remaining_turns]
        
        # A[j] を掛けて実際のりんご数にする
        return base_weight * self.input_data.A[j]

# --- クラス定義: ゲームの状態管理 ---
class GameState:
    def __init__(self, input_data: ProblemInput):
        self.input_data = input_data
        self.apples = input_data.K
        self.B = [[1 for _ in range(input_data.N)] for _ in range(input_data.L)]
        self.P = [[0 for _ in range(input_data.N)] for _ in range(input_data.L)]

    def get_upgrade_cost(self, i: int, j: int) -> int:
        return self.input_data.C[i][j] * (self.P[i][j] + 1)

    def process_turn(self, action: Optional[Tuple[int, int]]):
        N = self.input_data.N
        L = self.input_data.L
        A = self.input_data.A

        # 1. 行動フェーズ
        if action is not None:
            i, j = action
            cost = self.get_upgrade_cost(i, j)
            self.apples -= cost
            self.P[i][j] += 1

        # 2. 生産フェーズ
        # Level 0
        for j in range(N):
            self.apples += A[j] * self.B[0][j] * self.P[0][j]
        # Level 1以上
        for i in range(1, L):
            for j in range(N):
                self.B[i-1][j] += self.B[i][j] * self.P[i][j]

# --- 関数定義: 投資回収ソルバー ---
def solve():
    input_data = ProblemInput()
    analyzer = InvestmentAnalyzer(input_data)
    current_state = GameState(input_data)
    
    for t in range(input_data.T):
        best_action = None
        max_net_profit = -float('inf') # 最大純利益
        
        # 候補の探索
        # 何もしない(-1) は Profit 0 とみなす
        # ただし、今回は「正の利益が出るならやる」方針なので、
        # max_net_profit の初期値を 0 にすれば、自然と負の行動は選ばれなくなる。
        max_net_profit = 0
        
        for i in range(input_data.L):
            for j in range(input_data.N):
                cost = current_state.get_upgrade_cost(i, j)
                
                # お金が足りるかチェック
                if cost <= current_state.apples:
                    # 1. 得られる利益(Gain)を計算
                    gain = analyzer.get_gain(i, j, t)
                    
                    # 2. 純利益(Net Profit)を計算
                    net_profit = gain - cost
                    
                    # 3. 最大値を更新するかチェック
                    if net_profit > max_net_profit:
                        max_net_profit = net_profit
                        best_action = (i, j)
        
        # 行動の実行
        current_state.process_turn(best_action)
        
        # 出力
        if best_action is None:
            print("-1")
        else:
            print(f"{best_action[0]} {best_action[1]}")
        
        sys.stdout.flush()

if __name__ == "__main__":
    solve()