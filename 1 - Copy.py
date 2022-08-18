from math import ceil

def maj(numbers, num_elems):
    if num_elems == 1:
        return numbers[0]
    leftmaj = maj(numbers[0:(num_elems//2)], num_elems//2)
    rightmaj = maj(numbers[(num_elems//2):], ceil(num_elems//2))

    if leftmaj == rightmaj:
        return leftmaj
    left_cnt = numbers.count(leftmaj)
    right_cnt = numbers.count(rightmaj)
    return leftmaj if left_cnt > right_cnt else rightmaj

num_elems = int(input())
numbers = []
numbers = list(map(int, input().split()))
if numbers.count(maj(numbers, num_elems)) > num_elems/2:
    print(1)
else:
    print(0)
