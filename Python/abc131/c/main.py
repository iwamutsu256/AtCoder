import math
a,b,c,d = map(int,input().split())

# cで割り切れる数
cc = b//c - (a-1)//c

# dで割り切れる数
dc = b//d - (a-1)//d

# cdのどちらでも割り切れる数

cdc = b//(math.lcm(c,d)) - (a-1)//(math.lcm(c,d))

print((b-(a-1)) - (cc+dc-cdc))