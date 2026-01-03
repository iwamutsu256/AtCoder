import bisect
N = int(input())
A = list(map(int,input().split()))
# 辞書を使いそう
# 順序保持、検索
# jの位置を決めてから、それより小さいもの、大きいものの個数を数える
# 3で割った商をキーにしたリスト
# ここには配列のインデックスが格納される
three_dict = {}
# 7で割った商をキーにしたリスト
seven_dict = {}
for i in range(N):
    if A[i] % 3 == 0:
        if str(A[i]//3) in three_dict:
            three_dict[str(A[i]//3)].append(i)
        else:
            three_dict[str(A[i]//3)] = [i]
    if A[i] % 7 == 0:
        if str(A[i]//7) in seven_dict:
            seven_dict[str(A[i]//7)].append(i)
        else:
            seven_dict[str(A[i]//7)] = [i]
count = 0
print(three_dict,seven_dict)
for j in range(N):
    if A[j] % 5 != 0:
        continue
    num = str(A[j] // 5)
    # print(num)
    if num not in three_dict or num not in seven_dict:
        continue
    # jが最小の場合、iとkが右側
    # iの個数
    min_count_i = len(three_dict[num]) - bisect.bisect_right(three_dict[num],j) + 1
    # kの個数
    min_count_k = len(seven_dict[num]) - bisect.bisect_right(seven_dict[num],j) + 1
    min_count = min_count_i * min_count_k
    max_count_i = bisect.bisect_left(three_dict[num],j)
    max_count_k = bisect.bisect_left(seven_dict[num],j)
    max_count = max_count_i * max_count_k
    count += min_count + max_count
print(count)
