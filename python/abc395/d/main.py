N,Q = map(int,input().split())
#i番目に鳩iの場所(箱番号)
hato = [int(x) for x in range(N)]
#i番のラベルが入っている箱
label_box = [int(x) for x in range(N)]
#i番目の箱に入っているラベル
box_label = [int(x) for x in range(N)]
#print(S,T)
for i in range(Q):
    op = list(map(int,input().split()))
    if op[0] == 1:
        #鳩の居場所を更新
        hato[op[1]-1] = label_box[op[2]-1]
    elif op[0] == 2:
        #巣の参照を入れ替える
        box_label[label_box[op[1]-1]],box_label[label_box[op[2]-1]] = box_label[label_box[op[2]-1]],box_label[label_box[op[1]-1]]
        label_box[op[1]-1],label_box[op[2]-1] = label_box[op[2]-1],label_box[op[1]-1]
    else:
        print(box_label[hato[op[1]-1]]+1)
