N = int(input())
A = list(map(int,input().split()))
max_L = sum(A)
# 約数の列挙
yakusuu = []
for i in range(2,int(max_L**0.5) + 1):
    if max_L % i == 0:
        yakusuu.append(max_L // i)
# print(yakusuu)
length_dict = dict()
for i in range(N):
    if A[i] in length_dict.keys():
        length_dict[A[i]] += 1
    else:
        length_dict[A[i]] = 1
# print(length_dict)
ans = []
for num in yakusuu:
    flag = True
    for j in length_dict.keys():
        if num - j in length_dict and length_dict[j] == length_dict[num - j]:
            pass
        elif j // 2 == num and length_dict[j] % 2 == 0:
            pass
        elif j == num:
            pass
        else:
            flag = False
    if flag:
        ans.append(num)
ans.sort()
print(" ".join(map(str,ans)))

"""
解説
Aをソートしても一般性を失わない
まず、すべてのAtCoderリコが２つに分かれた場合を考えると、
合計がすべて等しくなるには一番小さいほうから順と一番大きいほうから順がペアになる必要がある
ソートしてあるものを順に調べるだけなので、O(N)
次に、2つにわかれなかったAtCoderリコが存在する場合を考える
この時、分かれずに残ったものはAのうち一番大きいもののみなので、
それ以外を抜かしてすべてが２つに分かれた場合と同様に調べるO(N)
ソートがボトルネックO(NlogN)
"""