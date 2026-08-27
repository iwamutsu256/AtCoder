h,w = map(int,input().split())
c = [list(input()) for _ in range(h)]
ue = h-1
hidari = w-1
sita = 0
migi = 0
for i in range(h):
    for j in range(w):
        if c[i][j] == "#":
            ue = min(ue,i)
            hidari = min(hidari,j)
            sita = max(sita,i)
            migi = max(migi,j)
# print(ue,sita,hidari,migi)
for i in range(ue,sita+1):
    print("".join(c[i][hidari:migi+1]))