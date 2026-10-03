# import sys
# n,k = map(int,input().split())
# a = list(map(int,input().split()))


# class SegTree:
#     """
#     init(init_val, ide_ele): 配列init_valで初期化 O(N)
#     update(k, x): k番目の値をxに更新 O(logN)
#     query(l, r): 区間[l, r)をsegfuncしたものを返す O(logN)
#     """
#     def __init__(self, init_val, segfunc, ide_ele):
#         """
#         init_val: 配列の初期値
#         segfunc: 区間にしたい操作
#         ide_ele: 単位元
#         n: 要素数
#         num: n以上の最小の2のべき乗
#         tree: セグメント木(1-index)
#         """
#         n = len(init_val)
#         self.segfunc = segfunc
#         self.ide_ele = ide_ele
#         self.num = 1 << (n - 1).bit_length()
#         self.tree = [ide_ele] * 2 * self.num
#         # 配列の値を葉にセット
#         for i in range(n):
#             self.tree[self.num + i] = init_val[i]
#         # 構築していく
#         for i in range(self.num - 1, 0, -1):
#             self.tree[i] = self.segfunc(self.tree[2 * i], self.tree[2 * i + 1])
    
#     def update(self, k, x):
#         """
#         k番目の値をxに更新
#         k: index(0-index)
#         x: update value
#         """
#         k += self.num
#         self.tree[k] = x
#         while k > 1:
#             self.tree[k >> 1] = self.segfunc(self.tree[k], self.tree[k ^ 1])
#             k >>= 1

#     def query(self, l, r):
#         """
#         [l, r)のsegfuncしたものを得る
#         l: index(0-index)
#         r: index(0-index)
#         """
#         res = self.ide_ele

#         l += self.num
#         r += self.num
#         while l < r:
#             if l & 1:
#                 res = self.segfunc(res, self.tree[l])
#                 l += 1
#             if r & 1:
#                 res = self.segfunc(res, self.tree[r - 1])
#             l >>= 1
#             r >>= 1
#         return res


# seg_max = SegTree(a,max,-1)
# seg_min = SegTree(a,min,10**6)


# flag = False


# not_sorts = []

# for i in range(n-1):
#     if a[i] > a[i+1]:
#         not_sorts.append(i+1)

# # print(not_sorts)

# if len(not_sorts) == 0:
#     print("Yes")
#     sys.exit()

# for i in range(n-k+1):
#     if i == 0:
#         if seg_max.query(i,i+k) <= a[i+k] and not_sorts[-1] < i+k:
#             flag = True
#     elif i == n-k:
#         if a[i-1] <= seg_min.query(i,i+k) and not_sorts[0] >= i:
#             flag = True
#     elif a[i-1] <= seg_min.query(i,i+k) and seg_max.query(i,i+k) <= a[i+k] and not_sorts[-1] < i+k and not_sorts[0] >= i:
#         flag = True

# if flag:
#     print("Yes")
# else:
#     print("No")


import sys
n,k = map(int,input().split())
a = list(map(int,input().split()))


class SparseTable:
    def __init__(self, func=None):
        self.func = func
        self.table = []

    def load(self, l):
        self.n = len(l)
        if self.n == 0:
            return
        
        # テーブルの高さ（必要なレベル数）
        self.depth = self.n.bit_length()
        self.table = [[] for _ in range(self.depth)]
        
        # Level 0 (長さ 2^0 = 1 の区間)
        self.table[0] = list(l)
        
        # Level 1 以上を構築
        for curLevel in range(1, self.depth):
            prev = self.table[curLevel - 1]
            length = 1 << (curLevel - 1)  # 2^(curLevel - 1)
            
            # 参照可能な範囲まで埋める
            row_len = self.n - (1 << curLevel) + 1
            row = [None] * row_len
            for i in range(row_len):
                row[i] = self.func(prev[i], prev[i + length])
            self.table[curLevel] = row

    def query(self, l, r):  # 半開区間 [l, r)
        diff = r - l
        if diff <= 0:
            raise ValueError("Invalid range: r must be greater than l")
        if diff == 1:
            return self.table[0][l]
            
        # diff 以下の最大の2の倍数乗の指数 k (2^k <= diff)
        level = diff.bit_length() - 1
        return self.func(self.table[level][l], self.table[level][r - (1 << level)])

st_max = SparseTable(max)
st_min = SparseTable(min)

st_max.load(a)
st_min.load(a)

flag = False

not_sorts = []

for i in range(n-1):
    if a[i] > a[i+1]:
        not_sorts.append(i+1)

# print(not_sorts)

if len(not_sorts) == 0 or n == k:
    print("Yes")
    sys.exit()

for i in range(n-k+1):
    if i == 0:
        if st_max.query(i,i+k) <= st_min.query(i+k,n) and not_sorts[-1] < i+k:
            flag = True
    elif i == n-k:
        if st_max.query(0,i) <= st_min.query(i,i+k) and not_sorts[0] >= i:
            flag = True
    elif st_max.query(0,i) <= st_min.query(i,i+k) and st_max.query(i,i+k) <= st_min.query(i+k,n) and not_sorts[-1] < i+k and not_sorts[0] >= i:
        flag = True

if flag:
    print("Yes")
else:
    print("No")