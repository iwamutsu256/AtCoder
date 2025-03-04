S = [int(x) for x in input().split()]
if sorted(S) == S and S[0] >= 100 and S[-1] <= 675:
    for i in range(len(S)):
        if S[i] % 25 != 0:
            print("No")
            break
    else:
        print("Yes")
else:
    print("No")