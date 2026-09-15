a,b,w = map(int,input().split())

if w*1000 % b == 0:
    min_count = w*1000//b
else:
    min_count = w*1000//b + 1

max_count = w*1000//a

if 0 in [min_count,max_count] or min_count > max_count:
    print("UNSATISFIABLE")
else:
    print(min_count,max_count)