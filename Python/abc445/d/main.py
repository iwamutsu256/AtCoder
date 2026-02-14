from collections import deque

H,W,N = map(int,input().split())
P = []
for i in range(N):
    h,w = map(int,input().split())
    P.append((h,w,i))

PH = deque([(-1,-1,-1)] + sorted(P))
PW = deque([(-1,-1,-1)]+sorted(P,key=lambda x: x[1]))
# print(PH)
# print(PW)
is_pop = set()
part_H = PH.pop()
part_W = PW.pop()
now_H = H
now_W = W
ans = []
for i in range(N):
    if part_H[2] in is_pop:
        while part_H[2] in is_pop:
            part_H = PH.pop()
    if part_W[2] in is_pop:
        while part_W[2] in is_pop:
            part_W = PW.pop()
    # print(PH,PW)
    if part_H[0] == now_H:
        # print(part_H,now_H,now_W)
        ans.append((H-now_H+1,now_W - part_H[1]+1,part_H[2]))
        is_pop.add(part_H[2])
        now_W -= part_H[1]
        part_H = PH.pop()
    elif part_W[1] == now_W:
        # print(part_H, now_H, now_W)
        ans.append((H-now_H+1,1,part_W[2]))
        is_pop.add(part_W[2])
        now_H -= part_W[0]
        part_W = PW.pop()
    # print(is_pop)
ans.sort(key=lambda x:x[2])
for i in range(N):
    print(ans[i][0],ans[i][1])