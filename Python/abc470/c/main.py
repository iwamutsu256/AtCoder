n,q = map(int,input().split())
number_list = [0 for _ in range(n)]
sum = 0
bit_count = [0 for _ in range(20)]
min_bit_count = [0 for _ in range(20)]
for i in range(q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        x = query[1]-1
        before = number_list[x]
        after = number_list[x] + 1
        zero_to_one = bin(after&(-(before+1)))[2:]
        # print(zero_to_one)
        for j in range(len(zero_to_one)):
            bit_count[20-len(zero_to_one)+j] += 1
        one_to_zero = bin(before&(-(after+1)))[2:]
        for j in range(len(one_to_zero)):
            bit_count[20-len(one_to_zero)+j] -= 1
        number_list[x] += 1
    else:
        pass
    # 各桁の足し
    # print(bit_count)
    sum = 0
    for j in range(20):
        if bit_count[j] % 2 != 0:
            sum += 2**(19-j)
    print(sum)