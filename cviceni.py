from random import randint


def guess_number_human(upper_bound):
    r = randint(1, upper_bound)
    g = -1
    lb = 1
    ub = upper_bound

    while g != r:
        g = (lb + ub)//2
        print("Hádám", g)
        if g < r:
            print("Moje číslo je větší!")
            lb = g + 1
        if g > r:
            print("Moje číslo je menší!")
            ub = g - 1
    print("Uhodl jsi!")


def binary_search(needle, haystack):
    lb = 0
    ub = len(haystack)
    i = (ub + lb)//2
    while ub >= lb:
        if haystack[i] < needle:
            lb = i + 1
        elif haystack[i] > needle:
            ub = i - 1
        else:
            return i
        i = (ub + lb) // 2
    return -1


# hay = [1, 2, 5, 8, 9, 10, 23, 27, 31, 38, 42, 46, 54, 61, 66, 71, 75, 80, 87, 91]
# find = 3
# print(binary_search(find, hay) == hay.index(find))


def super_power(base, exp):

    output = base

    print(output, exp)

    if exp != 1:
        output *= super_power(base, exp // 2)
    return output*base


# print(super_power(2, 4))  # 128
# print(super_power(5, 16)) # 30517578125

def number_of_coins(amount, coins):
    number = 0
    coins.sort(reverse=True)
    for c in coins:
        while amount >= c:
            amount -= c
            number += 1
    return number


print(number_of_coins(46, [1, 2, 5, 10, 20, 50])) # 4
print(number_of_coins(6, [1, 3, 5]))              # 2
