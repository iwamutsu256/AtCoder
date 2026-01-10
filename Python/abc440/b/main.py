N = int(input())
T = list(map(int,input().split()))
S = [(T[i],i+1) for i in range(N)]
S.sort()
# print(S)
print(S[0][1],S[1][1],S[2][1])