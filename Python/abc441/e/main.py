N = int(input())
S = list(input())
plus_minus_AB = [0]
for i in range(N):
    if S[i] == "A":
        plus_minus_AB.append(plus_minus_AB[i]+1)
    elif S[i] == "B":
        plus_minus_AB.append(plus_minus_AB[i]-1)
    else:
        plus_minus_AB.append(plus_minus_AB[i])
# print(plus_minus_AB)
# plus_minus_ABに格納される数値は-N~Nなので、それぞれの個数をカウントする配列を用意する
# それとは別に、現在のplus_minus_AB未満の個数を保持する変数sumを用意する
# 現在のplus_minus_ABとひとつ前のplus_minus_ABは高々一つしか差がないので、その差分を足し引きする
sum = 0
ans = 0
counter = [0] * (2*N + 1)
# スタート地点に0が1つという情報がないと一つ目の比較先がない
counter[0] = 1
for i in range(1,N+1):
    if S[i-1] == "A":
        # ひとつ前のsumは現在のsumであるD未満の総和より一つDが小さいD-1未満の総和である。
        # なので、ひとつ前のsumにcounter[D-1]を足せばいい
        sum += counter[plus_minus_AB[i]-1]
    elif S[i-1] == "B":
        # ひとつ前のsumは現在のsumであるD未満の総和より一つDが大きいD+1未満の総和である。
        # なので、ひとつ前のsumからcounter[D]を引けばいい
        sum -= counter[plus_minus_AB[i]]
    # plus_minus_ABがDになる値の数
    counter[plus_minus_AB[i]] += 1
    
    ans += sum
print(ans)