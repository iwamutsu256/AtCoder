N = int(input())
S = [input() for _ in range(N)]
count = 0
sentence = set()
for i in range(N):
    for j in range(N):
        if i == j:
            pass
        else:
            if S[i] + S[j] in sentence:
                pass
            else:
                sentence.add(S[i]+S[j])
                count += 1
print(count)