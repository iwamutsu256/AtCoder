s = [""]+list(input())
n = int(input())
for i in range(n):
    l,r = map(int,input().split())
    s = s[:l] + list(reversed(s[l:r+1])) + s[r+1:]

print("".join(s[1:]))