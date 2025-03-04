N = int(input())
A = int(input())
# ここにプログラムを追記
for i in range(1,N+1):
    op ,B = input().split()
    B = int(B)
    if op == "+":
        A += B
        print(i,A)
    elif op == "-":
        A = A - B
        print(i,A)
    elif op == "*":
        A = A * B
        print(i,A)
    elif op == "/" and B != 0:
        A = A // B
        print(i,A)
    else:
        print("error")
        break