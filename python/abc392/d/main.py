N = int(input())

data = []
for _ in range(N):
    nums = list(map(int, input().split()))
    size = nums[0]
    elements = nums[1:]

    element_set = set(elements)

    freq = {}
    for num in elements:
        if num in freq:
            freq[num] += 1
        else:
            freq[num] = 1
    
    data.append((size, element_set, freq))

ans = 0

for i in range(N - 1):
    size_i, set_i, freq_i = data[i]
    for j in range(i + 1, N):
        size_j, set_j, freq_j = data[j]
        common_elements = set_i & set_j  
        
        q = 0
        for num in common_elements:
            prob_i = freq_i[num] / size_i
            prob_j = freq_j[num] / size_j
            q += prob_i * prob_j
        
        ans = max(ans, q)

print(ans)
