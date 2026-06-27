def check_top():
    for i in range(len(canvas)):
        if canvas[i][0] == "#":
            return False
    return True

def check_bottom():
    for i in range(len(canvas)):
        if canvas[i][-1] == "#":
            return False
    return True

H,W = map(int,input().split())
canvas = [list(input()) for _ in range(H)]
while canvas[0] == ["." for _ in range(W)]:
    canvas.pop(0)
while canvas[-1] == ["." for _ in range(W)]:
    canvas.pop()
# print(canvas)
while check_top():
    for i in range(len(canvas)):
        canvas[i].pop(0)
while check_bottom():
    for i in range(len(canvas)):
        canvas[i].pop()
for i in range(len(canvas)):
    print("".join(canvas[i]))