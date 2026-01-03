def ishappy(num):
    if num == 1:
        return True
    elif num not in dictionary:
        dictionary.add(num)
        num = str(num)
        count = 0
        for i in range(len(num)):
            count += int(num[i])**2
        return ishappy(count)
    else:
        return False


N = int(input())
dictionary = set()
if ishappy(N):
    print("Yes")
else:
    print("No")