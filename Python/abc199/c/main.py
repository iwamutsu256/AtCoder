n = int(input())
s = list(input())
q = int(input())
s = [s[:n],s[n:]]
zenhan = 0
for _ in range(q):
    t,a,b = map(int,input().split())
    if t == 2:
        zenhan ^= 1
    else:
        a,b = a-1,b-1
        if a < n and b < n:
            s[zenhan][a],s[zenhan][b] = s[zenhan][b],s[zenhan][a]
        elif a < n and b >= n:
            s[zenhan][a],s[zenhan^1][b-n] = s[zenhan^1][b-n],s[zenhan][a]
        else:
            s[zenhan^1][a-n],s[zenhan^1][b-n] = s[zenhan^1][b-n],s[zenhan^1][a-n]
s = s[zenhan] + s[zenhan^1]
print("".join(s))