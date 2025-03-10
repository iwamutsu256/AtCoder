Q = int(input())
stack = [0 for _ in range(100)]
for i in range(Q):
    queue = list(map(int,input().split()))
    if queue[0] == 1:
        stack.append(queue[1])
    else:
        print(stack.pop())
        