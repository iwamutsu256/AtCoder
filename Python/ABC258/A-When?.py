K= int(input())
H = 21
if K >= 60:
    H += 1
    K -= 60
if K < 10:
    K = "0"+str(K)
else:
    K = str(K)
print(str(H)+":"+K)