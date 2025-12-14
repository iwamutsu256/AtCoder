import sys
import heapq
from typing import List, Tuple, Optional

# --- 定数設定 ---
# 実行時間制限(2sec)に合わせて調整してください。
# TLE(時間切れ)になる場合は 50 程度に下げてください。
BEAM_WIDTH = 50

# --- クラス定義: 入力管理 ---
class ProblemInput:
    """
    問題の入力データと定数を管理するクラス。
    """
    def __init__(self):
        # 入力の読み込み
        # N: 機械の種類数, L: Level数, T: ターン数, K: 初期りんご数
        line1 = sys.stdin.readline().split()
        if not line1: return # 空入力対策
        self.N, self.L, self.T, self.K = map(int, line1)
        
        # Level 0 の生産能力 A
        self.A = list(map(int, sys.stdin.readline().split()))
        
        # 各Levelの初期コスト C
        self.C = []
        for _ in range(self.L):
            self.C.append(list(map(int, sys.stdin.readline().split())))

# --- クラス定義: ゲーム状態 ---
class GameState:
    """
    ゲームの盤面状態を表すクラス。
    """
    def __init__(self, input_data: ProblemInput):
        self.input_data = input_data
        self.apples = input_data.K
        
        # B[i][j]: Level i, ID j の機械の数
        self.B = [[1] * input_data.N for _ in range(input_data.L)]
        
        # P[i][j]: Level i, ID j の機械のパワー
        self.P = [[0] * input_data.N for _ in range(input_data.L)]
        
        # 行動履歴 (turn, i, j)
        # 何もしない場合は (-1, -1)
        self.history: List[Tuple[int, int]] = [] 

    def copy(self) -> 'GameState':
        """状態のディープコピーを作成"""
        new_state = GameState(self.input_data)
        new_state.apples = self.apples
        # リストの内包表記で高速コピー
        new_state.B = [row[:] for row in self.B]
        new_state.P = [row[:] for row in self.P]
        new_state.history = self.history[:] # 履歴もコピー
        return new_state

    def evaluate(self, current_turn: int) -> float:
        """
        評価関数:
        現在の生産能力で残りターンを走り切った場合の推定最終りんご数。
        """
        remaining_turns = self.input_data.T - current_turn
        if remaining_turns <= 0:
            return self.apples

        # 現在の資産
        predicted_apples = self.apples
        
        # Level 0の1ターンあたりの生産力
        level0_prod_per_turn = 0
        for j in range(self.input_data.N):
            level0_prod_per_turn += self.input_data.A[j] * self.B[0][j] * self.P[0][j]
            
        # 簡易評価: 現在の生産力 × 残りターン
        predicted_apples += level0_prod_per_turn * remaining_turns
        
        return predicted_apples

    def get_upgrade_cost(self, i: int, j: int) -> int:
        return self.input_data.C[i][j] * (self.P[i][j] + 1)

# --- 関数定義: ターン処理ロジック ---
def process_turn_mechanic(state: GameState, input_data: ProblemInput):
    """
    1ターン分の生産・成長処理を行う。
    （行動によるコスト支払いやパワーアップは呼び出し元で済ませておくこと）
    """
    N, L = input_data.N, input_data.L
    A = input_data.A
    
    # Level 0 生産
    production = 0
    for j in range(N):
        production += A[j] * state.B[0][j] * state.P[0][j]
    state.apples += production
    
    # Level 1以上 生産
    # 問題文: Level 0, 1, 2... の順に処理
    # 下位レベルの機械数 B を増やす
    for i in range(1, L):
        for j in range(N):
            produced_count = state.B[i][j] * state.P[i][j]
            state.B[i-1][j] += produced_count

# --- 関数定義: ビームサーチソルバー ---
def solve():
    # 入力受付
    try:
        input_data = ProblemInput()
    except ValueError:
        return # 入力が空などの場合終了

    # 初期状態
    initial_state = GameState(input_data)
    
    # ビーム（現在のターンにおける有望な状態のリスト）
    current_beam = [initial_state]
    
    # Tターン回す
    for t in range(input_data.T):
        next_beam_candidates = []
        candidate_counter = 0 # 【修正点】同点時の比較回避用カウンタ
        
        # ビーム内の各状態について、次の手を探索
        for state in current_beam:
            
            # --- 選択肢1: 何もしない ---
            next_state_no_act = state.copy()
            # 行動処理なし（コスト支払いなし）
            process_turn_mechanic(next_state_no_act, input_data)
            next_state_no_act.history.append((-1, -1))
            
            score = next_state_no_act.evaluate(t + 1)
            # heapには (優先度, カウンタ, 状態) を入れる
            # 優先度は小さい順に取り出されるため、スコアが高いほど優先されるようマイナスをつける
            next_beam_candidates.append((-score, candidate_counter, next_state_no_act))
            candidate_counter += 1
            
            # --- 選択肢2: 強化可能なものを強化 ---
            # すべてを試すと遅くなる可能性があるが、N*L=40なので
            # ビーム幅200なら 40 * 200 = 8000状態/ターン。
            # T=500なので 4,000,000回程度の計算。Pythonだとギリギリか？
            # 間に合わなければ BEAM_WIDTH を下げる。
            
            for i in range(input_data.L):
                for j in range(input_data.N):
                    cost = state.get_upgrade_cost(i, j)
                    if cost <= state.apples:
                        next_state_act = state.copy()
                        
                        # コスト支払い & パワーアップ
                        next_state_act.apples -= cost
                        next_state_act.P[i][j] += 1
                        
                        # ターン処理（生産）
                        process_turn_mechanic(next_state_act, input_data)
                        next_state_act.history.append((i, j))
                        
                        score = next_state_act.evaluate(t + 1)
                        next_beam_candidates.append((-score, candidate_counter, next_state_act))
                        candidate_counter += 1

        # ソートして上位 BEAM_WIDTH 個を選択
        if len(next_beam_candidates) > BEAM_WIDTH:
            selected = heapq.nsmallest(BEAM_WIDTH, next_beam_candidates)
        else:
            selected = next_beam_candidates
            
        # 次のターンのビームを構築
        # selected の要素は (-score, counter, state) なので、state (index 2) を取り出す
        current_beam = [item[2] for item in selected]

    # 最終結果の選定
    # current_beam は予測スコア順に並んでいるが、
    # 最終ターン終了時は「実際のりんご数」でソートし直すのが確実
    current_beam.sort(key=lambda s: s.apples, reverse=True)
    best_state = current_beam[0]

    # 結果出力
    for action in best_state.history:
        if action == (-1, -1):
            print("-1")
        else:
            print(f"{action[0]} {action[1]}")
    
    sys.stdout.flush()

if __name__ == "__main__":
    # 再帰上限を念のため上げておく（今回は使わないが念のため）
    sys.setrecursionlimit(2000)
    solve()