N,M = map(int,input().split())
S = set(list(input()))
T = set(list(input()))
alphabet = {"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"}
not_takahasi = alphabet - S
not_aoki = alphabet - T
Q = int(input())
for _ in range(Q):
    w = list(input())
    flag_takahasi = True
    flag_aoki = True
    for i in w:
        if i in not_takahasi:
            flag_takahasi = False
        if i in not_aoki:
            flag_aoki = False
    if flag_takahasi and flag_aoki:
        print("Unknown")
    elif flag_takahasi:
        print("Takahashi")
    else:
        print("Aoki")