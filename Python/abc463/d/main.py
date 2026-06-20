# def kasane(i,j):
#     if nuno[i][0] > nuno[j][1] or nuno[i][1] < nuno[j][0]:
#         return False
#     else:
#         return True

# def score(i,j):
#     if kasane(i,j):
#         return -1
#     return min(abs(nuno[i][0]-nuno[j][1]),abs(nuno[i][1]-nuno[j][0]))

def solve(score):
    # first = 0
    last= nuno2[0][1]
    nuno2_index = 0
    for i in range(K-1):
        # L > 前回のR+score　のうち、Rが最小のものを貪欲に選択
        while nuno2_index < len(nuno2) and nuno2[nuno2_index][0] < last + score:
            nuno2_index += 1
        if nuno2_index == len(nuno2):
            return False
        last = nuno2[nuno2_index][1]
    else:
        return True

N,K = map(int,input().split())
nuno = [list(map(int,input().split())) for _ in range(N)]
nuno2 = nuno.copy()
nuno2.sort(key=lambda x: x[1])
# 答えで２分探索
# 貪欲
left = -1
right = 10**9 + 1
while right - left > 1:
    mid = left + (right - left)//2
    if solve(mid):
        left = mid
    else:
        right = mid
if left == -1 or left == 0:
    print(-1)
else:
    print(left)


