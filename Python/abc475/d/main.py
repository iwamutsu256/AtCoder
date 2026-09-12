import math
import itertools

def sieve_of_eratosthenes(n):
    prime = [True for i in range(n+1)]
    prime[0] = False
    prime[1] = False

    sqrt_n = math.ceil(math.sqrt(n))
    for i in range(2, sqrt_n):
        if prime[i]:
            for j in range(2*i, n+1, i):
                prime[j] = False

    return prime

# 素数の列挙
prime = sieve_of_eratosthenes(10**7-1)
# for p in range(10**7):
#     if prime[p]:
#         print(p, end=' ')

s = input()
t = sorted(set(s), key=s.index)
u = dict()
for i in range(len(s)):
    u[i] = t.index(s[i])
nums = [1,2,3,4,5,6,7,8,9,0]

for v in itertools.permutations(nums, len(t)):
    # print(v)
    if v[0] == 0:
        continue
    now = 0
    # print(v)
    for i in range(len(s)):
        now += v[u[i]]
        if i != len(s)-1:
            now *= 10
    # print(now)
    if prime[now]:
        print(now)
        break
else:
    print(-1)

