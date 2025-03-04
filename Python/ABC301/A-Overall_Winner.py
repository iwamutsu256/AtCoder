N = int(input())
S = input()
if S.count("A") < S.count("T"):
    print("T")
elif S.count("A") > S.count("T"):
    print("A")
else:
    if S.rfind("A") < S.rfind("T"):
        print("A")
    else:
        print("T")
