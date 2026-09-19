class sparseTable(object):
    func = None
    depthTreeList: int = 0
    table = []

    def load(self, l):
        self.n = len(l)
        self.depthTreeList = (self.n - 1).bit_length()
        self.table.append(l)
        # print(l)
        for curLevel in range(1, self.depthTreeList):
            l = []
            for i in range( self.n - (2**curLevel -1) ):
                l.append(self.func(self.table[curLevel - 1][i], self.table[curLevel - 1][i + (2**(curLevel - 1)) ] ))
            self.table.append(l)
            # print(l)

    def query(self, l, r): # [l, r)
        diff = r - l
        if diff <= 0:
            raise
        if diff == 1:
            return self.table[0][l]
        level = (diff - 1).bit_length() - 1
        return self.func(self.table[level][l], self.table[level][r - (2 ** level)])

n = int(input())
a = list(map(int,input().split()))

class sparseTableMin(sparseTable):
    func = min

st = sparseTableMin()
st.load(a)

ans = 0

for i in range(n):
    for j in range(i+1,n+1):
        ans = max(st.query(i,j)*(j-i),ans)

print(ans)
