class UnionFind:
    def __init__(self, n):
        self.parents = [-1] * n
    
    def root(self, x):
        stack = []
        while self.parents[x] >= 0:
            stack.append(x)
            x = self.parents[x]
        for y in stack:
            self.parents[y] = x
        return x
    
    def union(self, x, y):
        x = self.root(x)
        y = self.root(y)
        if x == y:
            return
        if self.parents[x] > self.parents[y]:
            x,y = y,x
        self.parents[x] += self.parents[y]
        self.parents[y] = x

    def size(self, x):
        return -self.parents[self.root(x)]

    def same(self, x, y):
        return self.root(x) == self.root(y)

    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    def group_count(self):
        return len(self.roots())

n,m = map(int,input().split())
uf = UnionFind(n)
for i in range(m):
    a,b = map(int,input().split())
    uf.union(a-1,b-1)
print(uf.group_count()-1)