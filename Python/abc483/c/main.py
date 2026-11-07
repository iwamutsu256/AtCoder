##### segfunc#####
def segfunc(x, y):
    return max(x,y)
#################

##### ide_ele#####
ide_ele = -1
#################

class SegTree:
    """
    init(init_val, ide_ele): 配列init_valで初期化 O(N)
    update(k, x): k番目の値をxに更新 O(logN)
    query(l, r): 区間[l, r)をsegfuncしたものを返す O(logN)
    """
    def __init__(self, init_val, segfunc, ide_ele):
        """
        init_val: 配列の初期値
        segfunc: 区間にしたい操作
        ide_ele: 単位元
        n: 要素数
        num: n以上の最小の2のべき乗
        tree: セグメント木(1-index)
        """
        n = len(init_val)
        self.segfunc = segfunc
        self.ide_ele = ide_ele
        self.num = 1 << (n - 1).bit_length()
        self.tree = [ide_ele] * 2 * self.num
        # 配列の値を葉にセット
        for i in range(n):
            self.tree[self.num + i] = init_val[i]
        # 構築していく
        for i in range(self.num - 1, 0, -1):
            self.tree[i] = self.segfunc(self.tree[2 * i], self.tree[2 * i + 1])
    
    def update(self, k, x):
        """
        k番目の値をxに更新
        k: index(0-index)
        x: update value
        """
        k += self.num
        self.tree[k] = x
        while k > 1:
            self.tree[k >> 1] = self.segfunc(self.tree[k], self.tree[k ^ 1])
            k >>= 1

    def query(self, l, r):
        """
        [l, r)のsegfuncしたものを得る
        l: index(0-index)
        r: index(0-index)
        """
        res = self.ide_ele

        l += self.num
        r += self.num
        while l < r:
            if l & 1:
                res = self.segfunc(res, self.tree[l])
                l += 1
            if r & 1:
                res = self.segfunc(res, self.tree[r - 1])
            l >>= 1
            r >>= 1
        return res

n,m = map(int,input().split())


election = []
for i in range(m):
    x,y = map(int,input().split())
    election.append((x,y))

election.sort()
# print(election)

sub = list(map(lambda x: x[0], election))
# print(sub)

points = [0 for _ in range(n+1)]
for i in sub:
    points[i] += 1
# print(points)

B = 10**6
p_max = list(map(lambda x: x*B, points))
for i in range(len(p_max)):
    p_max[i] += len(p_max)-i
# print(p_max)

st = SegTree(p_max,max,-1)

# move = points[:]

index = 0
for i in range(1,n+1):
    # move = points[:]
    for j in range(index,index+points[i]):
        if j == len(election):
            continue
        # print(j)
        # move[election[j][1]] += 1
        st.update(election[j][1],st.query(election[j][1],election[j][1]+1)+B)
    # print(points)
    # print(index)
    print(len(p_max) - (st.query(0,len(points))%B))
    for j in range(index,index+points[i]):
        if j == len(election):
            continue
        # print(j)
        # move[election[j][1]] += 1
        st.update(election[j][1],st.query(election[j][1],election[j][1]+1)-B)
    index += points[i]