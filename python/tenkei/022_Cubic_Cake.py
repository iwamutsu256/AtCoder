import math
A,B,C = map(int,input().split())
g = math.gcd(A,B,C)
print(((A//g)-1)+((B//g)-1)+((C//g)-1))