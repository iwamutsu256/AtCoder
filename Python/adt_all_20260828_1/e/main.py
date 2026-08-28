from itertools import permutations
s,k = input().split()
k = int(k)
words = set()
s = list(s)
for word in permutations(s,len(s)):
    word = "".join(word)
    words.add(word)
words = list(words)
words.sort()
print(words[k-1])