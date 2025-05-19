import random
import time
import math
import sys
N,M,L = map(int,input().split())
S = ["" for _ in range(N)]
P = [0 for _ in range(N)]
# S,Pを配列に保存 
for i in range(N):
    S[i],P[i] = input().split()
    S[i] = list(S[i])
    P[i] = int(P[i])
# 初期解
A = []
for i in range(12):
    A.append([9,9,9,9,8,8,8,8,8,8,8,8])
# aa,bb,cc,dd,ee,ffの順

# ポイント上位いくつかの文字列
Q = sorted(P,reverse=True)
# 個々の数字で上位何個かが変わる
Q = Q[:3]
R = []
Z = []
for i in range(N):
    if P[i] in Q:
        R.append(S[i])
        Z.append(P[i])

def get_score():
    score = 0
    for i in range(len(R)):
        # 遷移は同じ文字で２種類あるが、xとyと置く
        dp = [[0 for _ in range(2)] for _ in range(len(R[i]))]
        dp[0][0] = 1
        dp[0][1] = 1
        for j in range(1,len(R[i])):
            dp[j][0] = dp[j-1][0]*A[(ord(R[i][j-1])-97)*2][(ord(R[i][j])-97)*2]/100 + dp[j-1][1]*A[(ord(R[i][j-1])-97)*2+1][(ord(R[i][j])-97)*2]/100
            dp[j][1] = dp[j-1][0]*A[(ord(R[i][j-1])-97)*2][(ord(R[i][j])-97)*2+1]/100 + dp[j-1][1]*A[(ord(R[i][j-1])-97)*2+1][(ord(R[i][j])-97)*2+1]/100
        score += (dp[len(R[i])-1][0] + dp[len(R[i])-1][1])*Z[i]
    return score*10000


def hill():
    current_score = get_score()
    random.seed(42)
    start_time = time.time()
    time_limit = 1.7
    iteration = 0
    while True:
        current_time = time.time()
        if current_time - start_time >= time_limit:
            break
        # ランダムな状態を選ぶ
        i = random.randrange(0,12)
        # ランダムに確率を１％減らす場所を選ぶ
        j = random.randrange(0,12)
        if A[i][j] == 0:
            while A[i][j] == 0:
                j = random.randrange(0,12)
        # ランダムに確率を1%増やす場所を選ぶ
        k = random.randrange(0,12)
        A[i][j] -= 1
        A[i][k] += 1
        new_point = get_score()
        if new_point >= current_score:
            #print(f"iteration: {iteration},score: {new_point}", file=sys.stderr)
            current_score = new_point
        else:
            A[i][j] += 1
            A[i][k] -= 1
        iteration += 1
        if iteration % 1000 == 0:
            print(f"iteration: {iteration},score: {new_point}", file=sys.stderr)
    print("---Result---", file=sys.stderr)
    print("iteration     :",iteration, file=sys.stderr)
    print("total score: ",current_score, file=sys.stderr)

def result_print():
    for i in range(12):
        print(chr(math.floor(i/2)+97)," ".join(map(str,A[i])))

hill()
result_print()