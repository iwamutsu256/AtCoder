"""
左端の見つけ方
一番左から順に一つ右と比較して、一つ右の文字が今の文字より早いならそこで決定
右端の見つけ方
左端として決定された文字を比較元として、左端から順に右と比較して、早いなら交換、遅いならその前で決定
"""
T = int(input())
for _ in range(T):
    N = int(input())
    S = list(input())
    faze = 0
    L = 0
    R = 0
    for i in range(len(S)):
        if faze == 0: # 左端を見つける段階
            if i+1 < len(S) and ord(S[i]) > ord(S[i+1]):
                L = i
                faze = 1
            elif i == len(S)-1:
                L = i
                R = i
                faze = 2
            else:
                pass
        elif faze == 1: # 右端を見つける段階
            if i+1 < len(S) and ord(S[L]) < ord(S[i]):
                R = i
                faze = 2
            elif i == len(S)-1:
                if ord(S[L]) < ord(S[i]):
                    R = i
                else:
                    R = i+1
                faze = 2
            else:
                pass
        elif faze == 2: # 決まり終わってる
            break
    if R == len(S):
        S.append(S[L])
    else:
        S.insert(R,S[L])
    S.pop(L)
    print("".join(S))