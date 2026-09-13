from collections import deque
# 各高さでできるだけ長いレンガを使って敷き詰める


class State:
    def __init__(self, score, list, last_move, last_pos):
        self.score = score
        self.list = list
        self.last_move = last_move
        self.last_pos = last_pos

def set_block(start, list):
    if not list:
        score = 0
        path = []
        return [(score, path)]
    list = sorted(list)
    now_hole = list[0]
    one = set_block()

w, h, k = map(int,input().split())
cn = map(int,input().split())
holes = [tuple(map(int,input().split())) for _ in range(k)]

renga_count = 0
renga = []

h_holes = [[] for _ in range(h)]
for hole in holes:
    x,y = hole
    h_holes[y].append(x)

beam_width = 10000
beam = [None for _ in range(h)]



for i in range(h-1,-1,-1):
    # h_holes[i] = deque(sorted(h_holes[i]))
    # last = -1
    # if h_holes[i]:
    #     now = h_holes[i].popleft()
    # else:
    #     continue
    # while True:
    #     if h_holes[i]:
    #         next = h_holes[i].popleft()
    #     else:
    #         renga.append((now,i,1))
    #         last = now
    #         renga_count += 1
    #         if i > 0 and now not in h_holes[i-1]:
    #             h_holes[i-1].append(now)
    #         break
    #     renga_len = 1
    #     while True:
    #         if next - now + 1 <= 3 and (now+3 <= w or next - last >= 3):
    #             renga_len = 3
    #         elif next - now + 1 <= 5 and (now+5 <= w or next - last >= 5):
    #             renga_len = 5
    #         elif next - now + 1 <= 7 and (now+7 <= w or next - last >= 7):
    #             renga_len = 7
    #         elif next - now + 1 <= 9 and (now+9 <= w or next - last >= 9):
    #             renga_len = 9
    #         else:
    #             break
    #         if h_holes[i]:
    #             next = h_holes[i].popleft()
    #         else:
    #             next = -1
    #             break
    #     haiti_x = now
    #     if now + renga_len <= w:
    #         renga.append((now,i,renga_len))
    #     else:
    #         renga.append((w-renga_len,i,renga_len))
    #         haiti_x = w-renga_len
    #     last = now+renga_len-1
    #     renga_count += 1
    #     if i > 0 and (haiti_x+(haiti_x+renga_len-1))//2 not in h_holes[i-1]:
    #         h_holes[i-1].append((haiti_x + (haiti_x+renga_len-1))//2)
    #     if next != -1:
    #         now = next
    #     else:
    #         break

print(renga_count)
for i in range(renga_count):
    print(*renga[i])