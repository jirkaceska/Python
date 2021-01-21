import random
import math

def rand_list(n, a, b):
    output = []
    for i in range(n):
        output.append(random.randint(a, b))
    return output

def print_list(array):
    for i in range(len(array) - 1):
        print(array[i], end=", ")
    print(array[-1])

#rand = rand_list(3, 1, 10)
#print_list(rand)

def max_list(array):
    possible_max = array[0]
    for i in range(len(array)):
        if array[i] > possible_max:
            possible_max = array[i]
    print(possible_max)

# Dokončit!!
def unique(array):
    for i in range(len(array)):
        j = i + 1
        while j < len(array):
            while array[i] == array[j]:
                del array[j]
            j += 1
    return array
#print(unique([1,2,3,4,5,9,4,8,1,1,2, 9, 3,7]))


def count(a, array):
    counter = 0
    for i in range(len(array)):
        if array[i] == a:
            counter += 1
    return counter

def sum_list(array):
    return sum(array)

def is_prime_number(p):
    number_try = 7
    if p < 2:
        return False
    upper_boundary = int((number_try + p - abs(p - number_try))/2)
    for i in range(1, upper_boundary):
        if math.pow(i, p - 1) % p != 1:
            return False
    return True

def prime_numbers(bottom, length):
    for i in range(bottom, bottom + length + 1):
        print(i, is_prime_number(i), sep = ", ")

def divide_to_powers(n):
    helper = n
    output = []
    while helper >= 2:
        output.append(2)
        helper = helper // 2
    rest = n - math.pow(2, len(output))
    print(rest)
    if rest >= 2:
        output.append(divide_to_powers(rest))
    elif rest > 0:
        output.append(rest)
    return output

a = 533059705306690
#prime_numbers(a, 20)
#is_prime_number(100)
print(divide_to_powers(100))

def modulo_5(n):
    powers = divide_to_power(n)
