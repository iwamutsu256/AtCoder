def conbi(n):
    if n == 0 or n == 1:
        return 0
    else:
        return n*(n-1)//2

N,D = map(int,input().split())
person = [list(map(int,input().split())) for _ in range(N)]
time = [0 for _ in range(10**6+1)]
for i in range(N):
    [start,goal] = person[i]
    if goal - start < D:
        continue
    time[start] += 1
    time[goal-D+1] -= 1
# 累積和
person_count = [0 for _ in range(10**6+1)]
for i in range(1,len(person_count)):
    person_count[i] = person_count[i-1] + time[i]

count = 0
for i in range(1,len(person_count)):
    count += conbi(person_count[i])
print(count)