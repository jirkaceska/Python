from math import sqrt

def Pythagor(a, b):
    c = sqrt(a**2 + b**2)
    print(c)

def linear_series(length, multiples = 1):
    if length <= 0:
        return
    for i in range(1 * multiples, length * multiples, 1 * multiples):
        print(i, end = "*")
    print(length * multiples)

def repeat_series(length, boundary = None):
    counter = 0
    if length <= 0:
        return
    for i in range(1, length + 1):
        for j in range(1, i + 1):
            if boundary and counter == boundary:
                return
            print(j, end = " ")
            counter += 1

def fibonacci(length, a_1 = 0, a_2 = 1):
    if length == 0:
        return
    print(a_2, end = " ")
    fibonacci(length - 1, a_2, a_1 + a_2)

def traffic_line(dimension):
    for i in range(dimension):
        for j in range(dimension):
            if j == dimension//2 or j == 0 or j == dimension - 1:
                print ("#", end = " ")
            else:
                print(".", end = " ")
        print()

def chessboard(dimension):
    for i in range(dimension):
        for j in range(dimension):
            if (i + j) % 2 == 0:
                print (".", end = " ")
            else:
                print("#", end = " ")
        print()

def circle(r):
    for i in range(-r, r + 1):
        for j in range(-r, r + 1):
            if i**2 + j**2 <= r**2:
                print ("#", end = " ")
            else:
                print(".", end = " ")
        print()
circle(5)
