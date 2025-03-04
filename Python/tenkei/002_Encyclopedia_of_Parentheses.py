N = int(input())
l = [[] for _ in range(N)]
if N % 2 == 1:
    print()
else:
    ans = set()
    for bit in range(2**(N)):
        m = []
        for i in range(N):
            if bit & (2**i):
                m.append(1)
            else:
                m.append(-1)
            if sum(m) < 0:
                break
        c = ""
        if sum(m) == 0:
            for i in range(len(m)):
                if m[i] == 1:
                    c += "("
                else:
                    c += ")"
            if len(c) == N:
                ans.add(c)
    answer = list(ans)
    answer.sort()
    for i in range(len(answer)):
        print(answer[i])