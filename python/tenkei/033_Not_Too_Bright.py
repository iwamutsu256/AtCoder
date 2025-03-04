H,W = map(int,input().split())
if H % 2 == 0:
    h = H // 2
else:
    h = H // 2 + 1
if W % 2 == 0:
    w = W // 2
else:
    w = W // 2 + 1
if H != 1 and W != 1:
    print(h*w)
elif H == 1:
    print(W)
else:
    print(H)