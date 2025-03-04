N = int(input())
S = input()
sum = 0
for i in range(N-2):
    if S[i:i+3] == "#.#":
        sum += 1
print(sum)