n = int(input())
num = [0 for _ in range(n+1)]
start = 1
end = 2
while end != n+1:
    query = f"? {start} {end}"
    print(query, flush=True)
    answer = input()
    if answer == "Yes":
        end += 1
        num[start] = end - 1
    else:
        num[start] = end - 1
        start += 1
        if end == start:
            end += 1

# print(num)
current = 0
for i in range(len(num)):
    if num[i] < current:
        num[i] = current
    current = num[i]
# print(num)
count = 0
for i in range(len(num)):
    count += max(num[i] - i, 0)
print(f"! {count}", flush=True)