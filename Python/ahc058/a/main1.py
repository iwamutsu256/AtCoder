import sys
import math
from typing import List, Tuple, Optional

# --- クラス定義: 問題の定数や入力を管理 ---
class ProblemInput:
    """
    問題の入力データと定数を管理するクラスです。
    """
    def __init__(self):
        """
        標準入力からデータを読み込み、メンバ変数に格納します。
        """
        # 1行目の入力: N, L, T, K
        # N: 機械のIDの種類数 (10)
        # L: 機械のLevelの種類数 (4)
        # T: 総ターン数 (500)
        # K: 初期のりんごの数 (1)
        self.N, self.L, self.T, self.K = map(int, sys.stdin.readline().split())

        # 2行目の入力: Level 0 の機械の生産能力 A
        self.A = list(map(int, sys.stdin.readline().split()))

        # 続くL行: 各Levelの機械の初期コスト C
        # C[i][j] は Level i, ID j の機械のコスト
        self.C = []
        for _ in range(self.L):
            self.C.append(list(map(int, sys.stdin.readline().split())))

# --- クラス定義: ゲームの状態を管理 ---
class GameState:
    """
    ゲームの現在の状態（りんごの数、機械の数、機械のパワー）を管理し、
    シミュレーションを行うクラスです。
    """
    def __init__(self, input_data: ProblemInput):
        """
        初期状態を設定します。
        
        Args:
            input_data (ProblemInput): 問題の入力データ
        """
        self.input_data = input_data
        
        # 現在のりんごの数
        self.apples = input_data.K
        
        # 機械の個数 B[i][j] (初期値はすべて1)
        # Level i, ID j
        self.B = [[1 for _ in range(input_data.N)] for _ in range(input_data.L)]
        
        # 機械のパワー P[i][j] (初期値はすべて0)
        self.P = [[0 for _ in range(input_data.N)] for _ in range(input_data.L)]

    def copy(self) -> 'GameState':
        """
        現在の状態のディープコピーを作成して返します。
        シミュレーションで元の状態を破壊しないために使用します。
        
        Returns:
            GameState: 複製された状態
        """
        # __init__ を呼ばずにオブジェクトを作成し、必要な属性だけ複製する
        new_state = object.__new__(GameState)
        new_state.input_data = self.input_data
        new_state.apples = self.apples
        # リストの複製（深いコピー）
        new_state.B = [row[:] for row in self.B]
        new_state.P = [row[:] for row in self.P]
        return new_state

    def get_upgrade_cost(self, i: int, j: int) -> int:
        """
        指定された機械(i, j)を強化するための現在のコストを計算します。
        Cost = C[i][j] * (P[i][j] + 1)
        
        Args:
            i (int): Level
            j (int): ID
            
        Returns:
            int: 必要なコスト
        """
        return self.input_data.C[i][j] * (self.P[i][j] + 1)

    def process_turn(self, action: Optional[Tuple[int, int]]):
        """
        1ターン分の処理を進めます。
        1. 行動の実行（強化 または 何もしない）
        2. 生産の実行（Level順に処理）
        
        Args:
            action (Optional[Tuple[int, int]]): 
                強化する場合 (i, j) のタプル。
                何もしない場合 None。
        """
        N = self.input_data.N
        L = self.input_data.L
        A = self.input_data.A

        # --- 1. 行動フェーズ ---
        if action is not None:
            i, j = action
            cost = self.get_upgrade_cost(i, j)
            
            # コスト支払いとパワーアップ
            # 注: 呼び出し元でコスト不足のチェックを行う前提だが、念のためここでも引く
            self.apples -= cost
            self.P[i][j] += 1

        # --- 2. 生産フェーズ ---
        # Level 0, 1, 2, ... の順に処理
        
        # ローカル変数に束縛して属性アクセスを減らす（最適化）
        B = self.B
        P = self.P
        # Level 0: りんごの生産（増加量 = A[j] * B[0][j] * P[0][j])
        apple_production = 0
        b0 = B[0]
        p0 = P[0]
        for j in range(N):
            apple_production += A[j] * b0[j] * p0[j]
        self.apples += apple_production

        # Level 1以上: 下位Levelの機械の生産
        for i in range(1, L):
            bi = B[i]
            pi = P[i]
            b_prev = B[i-1]
            for j in range(N):
                b_prev[j] += bi[j] * pi[j]

# --- 関数定義: 貪欲法ソルバー ---
def solve():
    """
    メインのソルバー関数です。
    シミュレーションベースの貪欲法を実行します。
    """
    # 入力の読み込み
    input_data = ProblemInput()
    
    # 現在の状態
    current_state = GameState(input_data)
    
    # メインループ: 0ターン目からT-1ターン目まで
    for t in range(input_data.T):
        best_action = None
        # 初期スコアは「何もしない」を選んだ場合の予測値で初期化したいが、
        # 比較のために -1 に設定しておく（スコアは正なので）
        best_predicted_score = -1
        
        # 可能な行動の列挙: 全ての (i, j) について強化を検討
        # プラス、「何もしない」(-1) も検討
        
        # 候補リスト: (Level, ID) のタプル。None は「何もしない」
        candidates = [None]
        for i in range(input_data.L):
            for j in range(input_data.N):
                # コストチェック
                if current_state.get_upgrade_cost(i, j) <= current_state.apples:
                    candidates.append((i, j))
        
        # --- 貪欲法: 各候補についてシミュレーション ---
        for action in candidates:
            # 状態をコピーしてシミュレーションを行う
            sim_state = current_state.copy()
            
            # 1. 候補の行動をこのターンだけ実行
            sim_state.process_turn(action)
            
            # 2. 残りのターンは「何もしない」で進行させる
            remaining_turns = input_data.T - 1 - t
            
            # 高速化のため、詳細なループではなく簡易計算したいところだが、
            # 機械の個数が指数的に増えるため、正確にループを回す。
            # N=10, L=4 なのでループ内計算は軽い。
            for _ in range(remaining_turns):
                sim_state.process_turn(None)
            
            # 3. 評価値（最終的なりんごの数）を取得
            score = sim_state.apples
            
            # --- 貪欲法: 最大値の更新 ---
            if score > best_predicted_score:
                best_predicted_score = score
                best_action = action
            
            # 同点の場合は、コストが安い方やIDが小さい方を優先するなど
            # ブレークスルーがありうるが、今は単純に更新
            
        # 決定した行動を実行して、実際の状態を進める
        current_state.process_turn(best_action)
        
        # 出力
        if best_action is None:
            print("-1")
        else:
            print(f"{best_action[0]} {best_action[1]}")
        
        # 標準出力をフラッシュ（リアルタイムデバッグ用、提出時はなくてもよい）
        # 出力フラッシュは削除（毎ターンのflushが重い）

if __name__ == "__main__":
    solve()