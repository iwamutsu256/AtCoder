import sys

N, K, P, R = map(int, input().split())
patterns = [input().strip() for _ in range(P)]
for k in range(K):
    print(patterns[k])
sys.stdout.flush()

top = 0
for _ in range(R):
    request = int(input())
    if request == -1:
        sys.exit()
    count = (request - top) % K if request < K else 0
    print(count)
    for _ in range(count):
        print(top, K - 1)
        top = (top + 1) % K
    sys.stdout.flush()
