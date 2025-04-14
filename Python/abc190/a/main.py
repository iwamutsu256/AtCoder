A,B,C = map(int,input().split())
if A == B:
    if C == 0:
        print("Aoki")
    else:
        print("Takahashi")
else:
    if A < B:
        print("Aoki")
    else:
        print("Takahashi")