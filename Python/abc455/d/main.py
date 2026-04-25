N,Q = map(int,input().split())

# そのカードが現在どの山に所属しているか
current_place = dict()
for i in range(1,N+1):
    current_place[i] = i

# カードの山の一番下のカード
mountain_roots = [i for i in range(N+1)]

# 自分の上にいるカード
on_card = [None for _ in range(N+1)]

# 自分の下にいるカード
under_card = [None for _ in range(N+1)]

for _ in range(Q):
    C,P = map(int,input().split())
    if mountain_roots[current_place[C]] == C:
        mountain_roots[current_place[C]] = None
    else:
        on_card[under_card[C]] = None
    on_card[P] = C
    under_card[C] = P

ans = []
for i in range(1,N+1):
    if mountain_roots[i] == None:
        ans.append("0")
    else:
        count = 1
        current_card = mountain_roots[i]
        while on_card[current_card]:
            current_card = on_card[current_card]
            count += 1
        ans.append(str(count))
print(" ".join(ans))