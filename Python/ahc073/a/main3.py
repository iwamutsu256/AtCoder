import random

# インプット
n,m,k,t = map(int,input().split())
start = tuple(map(int,input().split()))
distinations = [start]+[tuple(map(int,input().split())) for _ in range(m)]

# 方針3
# 思ったほど改善されなかった
# 魔法陣の出現位置を変更させるべきだと思うが、途中地点を変更すると、それ以降が変更されてしまうので、
# 局所探索が難しい。
# よって、ビームサーチに挑戦する
# とりあえず、初めての実装なので、魔法陣[1,2,3]を使う、使わないの4択だけにする


# magic_circles = []

class State:
    def __init__(self, score, magic_circles, last_move, last_pos):
        self.score = score
        self.last_magic_circles = magic_circles
        self.last_move = last_move
        self.last_pos = last_pos

    def clone(self):
        return State(self.score, self.last_magic_circles, self.last_move, self.last_pos)

WIDTH = 1000
num_state = [0 for _ in range(m+1)]
beam = [[State(0,[],None, None) for _ in range(WIDTH)] for _ in range(m+1)]

act = [0 for _ in range(m+1)]

def beamsearch():
    # 0手目の状態を設定
    global num_state
    num_state[0] = 1
    beam[0][0].score = 0
    beam[0][0].last_magic_circles = [None for _ in range(k)]
    for i in range(k):
        randomy = random.randrange(n//4,n*3//4)
        randomx = random.randrange(n//4,n*3//4)
        beam[0][0].last_magic_circles[i] = (randomy,randomx)
    # ビームサーチ
    for i in range(1,m+1):
        candidate = []
        for j in range(num_state[i-1]):
            # 魔法陣1
            sousa1 = State(beam[i-1][j].score,beam[i-1][j].last_magic_circles[:],beam[i-1][j].last_move,beam[i-1][j].last_pos)
            # 操作の番号
            sousa1.last_move = 1
            sousa1.last_pos = j
            cy,cx = distinations[i-1]
            gy,gx = distinations[i]
            mcy,mcx = sousa1.last_magic_circles[0]
            sousa1.last_magic_circles[0] = distinations[i-1]
            if 0 <= (2*mcy - cy) < n and 0 <= (2*mcx - cx) < n:
                sousa1.score += abs(gy-(2*mcy - cy)) + abs(gx-(2*mcx - cx)) + 1
            else:
                sousa1.score += 10**9

            # 魔法陣2
            sousa2 = State(beam[i-1][j].score,beam[i-1][j].last_magic_circles[:],beam[i-1][j].last_move,beam[i-1][j].last_pos)
            # 操作の番号
            sousa2.last_move = 2
            sousa2.last_pos = j
            cy,cx = distinations[i-1]
            gy,gx = distinations[i]
            mcy,mcx = sousa2.last_magic_circles[1]
            sousa2.last_magic_circles[1] = distinations[i-1]
            if 0 <= (2*mcy - cy) < n and 0 <= (2*mcx - cx) < n:
                sousa2.score += abs(gy-(2*mcy - cy)) + abs(gx-(2*mcx - cx)) + 1
            else:
                sousa2.score += 10**9

            # 魔法陣3
            sousa3 = State(beam[i-1][j].score,beam[i-1][j].last_magic_circles[:],beam[i-1][j].last_move,beam[i-1][j].last_pos)
            # 操作の番号
            sousa3.last_move = 3
            sousa3.last_pos = j
            cy,cx = distinations[i-1]
            gy,gx = distinations[i]
            mcy,mcx = sousa3.last_magic_circles[2]
            sousa3.last_magic_circles[2] = distinations[i-1]
            if 0 <= (2*mcy - cy) < n and 0 <= (2*mcx - cx) < n:
                sousa3.score += abs(gy-(2*mcy - cy)) + abs(gx-(2*mcx - cx)) + 1
            else:
                sousa3.score += 10**9

            # 使わない
            sousa4 = State(beam[i-1][j].score,beam[i-1][j].last_magic_circles[:],beam[i-1][j].last_move,beam[i-1][j].last_pos)
            # 操作の番号
            sousa4.last_move = 4
            sousa4.last_pos = j
            cy,cx = distinations[i-1]
            gy,gx = distinations[i]
            sousa4.score += abs(gy-cy) + abs(gx-cx)

            candidate.append(sousa1)
            candidate.append(sousa2)
            candidate.append(sousa3)
            candidate.append(sousa4)
        candidate.sort(key=lambda x: x.score)
        num_state[i] = min(WIDTH, len(candidate))
        for j in range(num_state[i]):
            beam[i][j] = candidate[j]

def main():
    beamsearch()
    # print(beam)
    current_place = 0
    for i in range(m,0,-1):
        act[i] = beam[i][current_place].last_move
        current_place = beam[i][current_place].last_pos
    # print(act)
    for i in range(k):
        y,x = beam[0][0].last_magic_circles[i]
        print(y,x)

    magic_circles = beam[0][0].last_magic_circles.copy()
    
    cy, cx = start
    for i in range(1,m+1):
        gy,gx = distinations[i]
        if act[i] == 1:
            mcy,mcx = magic_circles[0]
            magic_circles[0] = (cy,cx)
            print("J",mcy,mcx)
            cy,cx = 2*mcy - cy, 2*mcx - cx
            for _ in range(abs(gx-cx)):
                if gx > cx:
                    print("R")
                    cx += 1
                else:
                    print("L")
                    cx -= 1
            for _ in range(abs(gy-cy)):
                if gy > cy:
                    print("D")
                    cy += 1
                else:
                    print("U")
                    cy -= 1
        elif act[i] == 2:
            mcy,mcx = magic_circles[1]
            magic_circles[1] = (cy,cx)
            print("J",mcy,mcx)
            cy,cx = 2*mcy - cy, 2*mcx - cx
            for _ in range(abs(gx-cx)):
                if gx > cx:
                    print("R")
                    cx += 1
                else:
                    print("L")
                    cx -= 1
            for _ in range(abs(gy-cy)):
                if gy > cy:
                    print("D")
                    cy += 1
                else:
                    print("U")
                    cy -= 1
        elif act[i] == 3:
            mcy,mcx = magic_circles[2]
            magic_circles[2] = (cy,cx)
            print("J",mcy,mcx)
            cy,cx = 2*mcy - cy, 2*mcx - cx
            for _ in range(abs(gx-cx)):
                if gx > cx:
                    print("R")
                    cx += 1
                else:
                    print("L")
                    cx -= 1
            for _ in range(abs(gy-cy)):
                if gy > cy:
                    print("D")
                    cy += 1
                else:
                    print("U")
                    cy -= 1
        else:
            for _ in range(abs(gx-cx)):
                if gx > cx:
                    print("R")
                    cx += 1
                else:
                    print("L")
                    cx -= 1
            for _ in range(abs(gy-cy)):
                if gy > cy:
                    print("D")
                    cy += 1
                else:
                    print("U")
                    cy -= 1

main()