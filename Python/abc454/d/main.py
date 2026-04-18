T = int(input())
for _ in range(T):
    A = list(input())
    B = list(input())
    stackA = []
    for i in A:
        stackA.append(i)
        if len(stackA) >= 4 and stackA[-4:] == ["(","x","x",")"]:
            stackA.pop()
            stackA.pop()
            stackA.pop()
            stackA.pop()
            stackA.append("x")
            stackA.append("x")
    stackB = []
    for i in B:
        stackB.append(i)
        if len(stackB) >= 4 and stackB[-4:] == ["(","x","x",")"]:
            stackB.pop()
            stackB.pop()
            stackB.pop()
            stackB.pop()
            stackB.append("x")
            stackB.append("x")
    # print("".join(stackA),"".join(stackB))
    if stackA == stackB:
        print("Yes")
    else:
        print("No")