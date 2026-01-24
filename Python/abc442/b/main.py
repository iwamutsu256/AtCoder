Q = int(input())
volume = 0
play = False
for i in range(Q):
    A = int(input())
    if A == 1:
        volume += 1
    elif A == 2:
        if volume > 0:
            volume -= 1
    else:
        play = not play
    if play and volume >= 3:
        print("Yes")
    else:
        print("No")
