# import heapq
N = int(input())
# k**2 < N までのリスト
square = []
for i in range(1,int(N**0.5)+1):
    square.append(i**2)
# h = []
first = set()
second = set()
for i in range(len(square)-1):
    for j in range(i+1,len(square)):
        if square[i] + square[j] <= N:
            if square[i] + square[j] not in first and square[i] + square[j] not in second:
                first.add(square[i] + square[j])
            elif square[i] + square[j] in first and square[i] + square[j] not in second:
                second.add(square[i] + square[j])
                first.remove(square[i] + square[j])
            else:
                continue
        else:
            break
ones = list(first)
ones.sort()
print(len(ones))
print(" ".join(map(str,ones)))