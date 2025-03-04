alp = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
S = list(input())
sum = 0
for i in range(len(alp)-1):
    d = abs(S.index(alp[i+1])-S.index(alp[i]))
    sum += d
print(sum)