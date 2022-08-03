# This problem is called "Maximum Number of Prizes". The goal of this problem is to represent a given
#  positive integer 𝑛 as a sum of as many pairwise distinct positive integers as possible. Problem solved
#  by the following greedy algorithm:

num = float(input("Enter an integer: "))
numTemp = num
i = 1
res = []
if num == 0:
    print("1\n0")
elif num == 1:
    print("1\n1")
elif num == 2:
    print("1\n2")
else:
    while True:
        numTemp -= i
        res.append(i)
        i += 1
        if numTemp - i <= i:
            last = num - sum(res)
            res.append(last)
            break
    print(f"'{num}' can be represented as a sum of {len(res)} numbers: {' '.join(map(str, res))}")