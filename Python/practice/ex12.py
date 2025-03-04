N = int(input())  # 生徒の数Nを読み込む
T = list(map(int, input().split()))  # 各生徒のゴールまでの時間を読み込む
# ここにプログラムを追記
U = sorted(T)
print(T.index(U[0])+1)