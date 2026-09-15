n = int(input())
a = [int(input()) for _ in range(n)]

paper = set()

for i in range(n):
    if a[i] in paper:
        paper.remove(a[i])
    else:
        paper.add(a[i])
print(len(paper))