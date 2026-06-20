# N = int(input())
# takahasi = [list(map(int,input().split())) for _ in range(N)]
# takahasi.sort()
# # print(takahasi)
# Q = int(input())
# T = list(map(int,input().split()))
# U = []
# for i in range(Q):
#     U.append([T[i],i])
# U.sort()
# # print(U)
# ans = []
# max_index = len(takahasi) - 1
# for i in range(Q):
#     while takahasi[max_index][1] <= U[i][0]:
#         max_index -= 1
#     ans.append([U[i][1],takahasi[max_index][0]])
# # print(" ".join(ans))
# # print(ans)
# ans.sort()
# print("\n".join(list(map(lambda x:str(x[1]),ans))))
# # for i in ans:
# #     print(i[1])

import bisect

N = int(input())
takahasi = [list(map(int,input().split())) for _ in range(N)]
takahasi.sort()
# print(takahasi)
Q = int(input())
T = list(map(int,input().split()))
max_index = len(takahasi) - 1
max_height = takahasi[max_index][0]
timeline = [[0,max_height]]
next_change_time = takahasi[max_index][1]
while max_index > -1:
    next_index = max_index - 1
    if next_index == -1:
        break
    while next_change_time >= takahasi[next_index][1]:
        next_index -= 1
        if next_index == -1:
            break
    if next_index == -1:
        break
    max_index = next_index
    max_height = takahasi[max_index][0]
    timeline.append([next_change_time,max_height])
    next_change_time = takahasi[max_index][1]

# print(timeline)

time = list(map(lambda x: x[0], timeline))

for i in range(Q):
    print(timeline[bisect.bisect_right(time,T[i])-1][1])


# # これでも行けた
# import sys

# # 高速な入力のための設定
# input = sys.stdin.read


# def solve():
#     # すべての入力を一度に読み込む
#     input_data = input().split()
#     if not input_data:
#         return

#     # ポインタを使ってパースしていく
#     ptr = 0

#     N = int(input_data[ptr])
#     ptr += 1

#     takahasi = []
#     for _ in range(N):
#         h = int(input_data[ptr])
#         l = int(input_data[ptr + 1])
#         takahasi.append([h, l])
#         ptr += 2

#     takahasi.sort()

#     Q = int(input_data[ptr])
#     ptr += 1

#     U = []
#     for i in range(Q):
#         t = int(input_data[ptr])
#         U.append([t, i])
#         ptr += 1

#     U.sort()

#     ans = []
#     max_index = len(takahasi) - 1

#     # あなたの完璧なロジック（そのまま）
#     for i in range(Q):
#         while takahasi[max_index][1] <= U[i][0]:
#             max_index -= 1
#         ans.append([U[i][1], takahasi[max_index][0]])

#     ans.sort()

#     # 出力を劇的に高速化（改行コードで結合して一度にプリント）
#     output = [str(i[1]) for i in ans]
#     sys.stdout.write("\n".join(output) + "\n")


# if __name__ == "__main__":
#     solve()