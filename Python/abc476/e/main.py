n,m = map(int,input().split())
p = list(map(int,input().split()))

q = [[p[i],i] for i in range(n)]

##### segfunc#####
def max_with_index(x,y):
    if x[0] > y[0]:
        return x
    else:
        return y

def min_with_index(x,y):
    if x[0] > y[0]:
        return y
    else:
        return x
#################

##### ide_ele#####
ide_ele_min = [float('inf'),-1]
ide_ele_max = [-float('inf'),-1]
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
        # print(self.tree)
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
        # print(f"k:{k},len(self.tree) = {len(self.tree)}")
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
                res = self.segfunc(res,self.tree[r - 1])
            l >>= 1
            r >>= 1
        return res


seg_min = SegTree(q,min_with_index,ide_ele_min)
seg_max = SegTree(q,max_with_index,ide_ele_max)

for i in range(m):
    l,r = map(int,input().split())
    l -= 1
    # r -= 1
    min_v,min_i = seg_min.query(l,r)
    max_v,max_i = seg_max.query(l,r)
    # print(f"min_i = {min_i},max_i:{max_i}")
    seg_min.update(min_i,[max_v,min_i])
    seg_min.update(max_i,[min_v,max_i])
    seg_max.update(min_i,[max_v,min_i])
    seg_max.update(max_i,[min_v,max_i])

ans = []
for i in range(n):
    ans.append(seg_max.query(i,i+1)[0])
print(*ans)