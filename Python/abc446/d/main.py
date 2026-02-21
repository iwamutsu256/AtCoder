# 解説を読みながら解きました。
from collections import defaultdict
# defaultdictは存在しないkeyを指定しても初期値を指定することができる
d = defaultdict(int)
# これは新しいkeyを指定した場合０で初期化する
# 引数には関数を指定することができ、lambda: int()と同じ
N = int(input())
A = list(map(int,input().split()))
for v in A:
    # 今の値をｖとして、新しく部分増加列を作成するか、v-1までに+1するかで長いほうを最長部分増加列とする
    d[v] = max(d[v], d[v-1] + 1)
# dの値のうち、最大のものが答えになる
print(max(d.values()))