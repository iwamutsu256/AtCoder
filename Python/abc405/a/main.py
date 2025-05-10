R,X = map(int,input().split())
if X == 1:
    if 1600 <= R and R <= 2999:
        print("Yes")
    else:
        print("No")
else:
    if 1200 <= R and R <= 2399:
        print("Yes")
    else:
        print("No")