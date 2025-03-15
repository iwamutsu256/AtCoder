N = int(input())
H = list(map(int,input().split()))
B = H.copy()
B.sort()
maximum = B[-1]
print(H.index(maximum)+1)