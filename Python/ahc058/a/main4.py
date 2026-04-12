import sys
import math
from typing import List, Tuple, Optional

# --- クラス定義: 入力管理 ---
class ProblemInput:
    def __init__(self):
        line1 = sys.stdin.readline().split()
        if not line1: return
        self.N, self.L, self.T, self.K = map(int, line1)
        self.A = list(map(int, sys.stdin.readline().split()))
        self.C = []
        for _ in range(self.L):
            self.C.append(list(map(int, sys.stdin.readline().split())))

# --- クラス定義: ゲーム状態 ---
class GameState:
    def __init__(self, input_data: ProblemInput):
        self.input_data = input_data
        self.apples = input_data.K
        # 機械の数 B[i][j]
        self.B = [[1] * input_data.N for _ in range(input_data.L)]
        # 機械のパワー P[i][j]
        self.P = [[0] * input_data.N for _ in range(input_data.L)]

    def copy(self) -> 'GameState':
        new_state = GameState(self.input_data)
        new_state.apples = self.apples
        new_state.B = [row[:] for row in self.B]
        new_state.P = [row[:] for row in self.P]
        return new_state

    def get_upgrade_cost(self, i: int, j: int) -> int:
        return self.input_data.C[i][j] * (self.P[i][j] + 1)

    def process_turn(self, action: Optional[Tuple[int, int]] = None):
        """1ターン進める（行動処理 -> 生産処理）"""
        # 行動によるコスト支払いと強化
        if action is not None:
            i, j = action
            cost = self.get_upgrade_cost(i, j)
            self.apples -= cost
            self.P[i][j] += 1

        # 生産処理
        N, L = self.input_data.N, self.input_data.L
        A = self.input_data.A

        # Level 0: りんご生産
        production = 0
        for j in range(N):
            production += A[j] * self.B[0][j] * self.P[0][j]
        self.apples += production

        # Level 1以上: 下位機械の生産
        for i in range(1, L):
            for j in range(N):
                produced = self.B[i][j] * self.P[i][j]
                self.B[i-1][j] += produced

# --- ヘルパー関数: 目標到達ターン数の計算 ---
def estimate_turns_to_reach_target(state: GameState, target_cost: int, max_turns: int) -> int:
    """
    現在の状態から「何もしない（貯金）」を続けた場合、
    target_cost に到達するまでに何ターンかかるかをシミュレーションで求める。
    """
    # すでに足りている場合
    if state.apples >= target_cost:
        return 0
    
    # シミュレーション用の一時状態（コピーはコストがかかるので、必要な変数だけ取り出す）
    # ただし、Bは毎ターン増えるので簡易計算は難しい。
    # ここは愚直にシミュレーションするが、高速化のためループ内で処理。
    
    current_apples = state.apples
    B = [row[:] for row in state.B]
    P = state.P # Pは変化しないので参照でOK
    A = state.input_data.A
    N, L = state.input_data.N, state.input_data.L
    
    for t in range(1, max_turns + 1):
        # 1. 生産
        # Level 0
        prod = 0
        for j in range(N):
            prod += A[j] * B[0][j] * P[0][j]
        current_apples += prod
        
        # 目標達成チェック
        if current_apples >= target_cost:
            return t
            
        # Level 1以上更新
        for i in range(1, L):
            for j in range(N):
                B[i-1][j] += B[i][j] * P[i][j]
                
    return max_turns + 1 # 届かなかった場合

# --- メインソルバー ---
def solve():
    try:
        input_data = ProblemInput()
    except:
        return

    # --- 戦略のターゲットを決める ---
    # A[j] が最も大きい機械の Level 3 (L-1) をターゲットにする
    # （もし同率ならコストが安い方などが良いが、Aはソート済みなので末尾を使う）
    target_j = input_data.N - 1
    target_i = input_data.L - 1
    
    # ターゲット: 機械(target_i, target_j)
    # 最初の1個を買うまでは「最短到達モード」
    target_acquired = False
    
    current_state = GameState(input_data)
    
    for t in range(input_data.T):
        best_action = None
        
        # --- モード分岐 ---
        
        # 1. ターゲット未購入モード: 「Level 3を買うまでのターン数」を最小化する
        if not target_acquired:
            
            # 現在のターゲットのコスト（変動しないはずだが一応取得）
            target_cost = current_state.get_upgrade_cost(target_i, target_j)
            
            # もし今買えるなら、即買い！
            if current_state.apples >= target_cost:
                best_action = (target_i, target_j)
                target_acquired = True # 次のターンからはモード切替
            else:
                # 買えない場合、「何もしない」vs「投資して加速」を比較
                
                # 基準: 何もしない場合の到達ターン数
                # 残りターン数以上かかるなら意味がないのでキャップを設ける
                remaining_turns = input_data.T - t
                base_turns = estimate_turns_to_reach_target(current_state, target_cost, remaining_turns)
                
                min_turns = base_turns
                best_action = None # デフォルトは何もしない
                
                # 全ての強化候補を試す
                for i in range(input_data.L):
                    for j in range(input_data.N):
                        # ターゲットそのものは買えないのでスキップ（上のifで弾いているが念のため）
                        if i == target_i and j == target_j:
                            continue
                            
                        cost = current_state.get_upgrade_cost(i, j)
                        
                        # 買えるものだけ検討
                        if cost <= current_state.apples:
                            # シミュレーション: 1回強化してみる
                            sim_state = current_state.copy()
                            sim_state.process_turn((i, j))
                            
                            # 強化による1ターン消費 + その後の到達ターン数
                            turns_after_act = estimate_turns_to_reach_target(sim_state, target_cost, remaining_turns)
                            total_turns = 1 + turns_after_act
                            
                            # より早く着くなら採用！
                            # 同着なら、コストが安い方やIDが小さい方を...今は単純更新
                            if total_turns < min_turns:
                                min_turns = total_turns
                                best_action = (i, j)
        
        # 2. ターゲット購入済みモード: Step 1と同様の「最終スコア最大化」
        # （せっかくLevel 3を手に入れたので、残りのターンでさらにスコアを伸ばす）
        else:
            best_predicted_score = -1
            best_action = None
            
            # 候補: 何もしない
            # （計算省略可だが、比較のため）
            sim_state = current_state.copy()
            # 残りターン何もしないシミュレーション
            remaining = input_data.T - 1 - t
            # 高速化のため、詳細シミュレーションは関数化すべきだが、
            # ここでは簡易的に「現在の生産力 × 残り」で評価
            # Step 1のコードのように真面目に回すと重いかもしれないので、
            # ここでは「何もしない」の評価は一旦保留し、投資効果だけ見る。
            
            # 常に「一番良い投資」を探す単純貪欲
            # 評価関数: (増える生産力 * 残りターン) - コスト
            
            max_roi = 0 # 投資対効果
            
            for i in range(input_data.L):
                for j in range(input_data.N):
                    cost = current_state.get_upgrade_cost(i, j)
                    if cost <= current_state.apples:
                        # 簡易ROI評価:
                        # この投資で、最終的なLevel 0の稼働回数がどれだけ増えるか？
                        # InvestmentAnalyzer の重みを使えば正確だが、
                        # ここではシンプルに「上位Levelほど強い」というヒューリスティックで選ぶ
                        # あるいは、Level 3が買えるならLevel 3を買う！
                        
                        # 簡易戦略: 買える一番高いLevelのものを買う
                        # Levelが同じなら A[j] が高い方
                        score = i * 1000 + input_data.A[j]
                        if score > max_roi:
                            max_roi = score
                            best_action = (i, j)
            
            # もし何も買えない、または効果が薄そうならNone（何もしない）
            # ここでは「買えるなら一番いいやつを買う」という豪遊モード
            
        # 行動実行
        current_state.process_turn(best_action)
        
        # 出力
        if best_action is None:
            print("-1")
        else:
            print(f"{best_action[0]} {best_action[1]}")
            
        sys.stdout.flush()

if __name__ == "__main__":
    solve()