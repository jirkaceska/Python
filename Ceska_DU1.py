import math
from turtle import Turtle

def flag(width):
    for i in range(1, 2*width):
        # Range width as max, then subtract abs from i - width
        # This expression reaches maximum for i == width, then descend)
        for j in range (width - abs(i - width)):
            print("*", end="")
        print()

def pyramid(height):
    for i in range(1, height + 1):
        for j in range(1, 2*height):
            # Print only in center of pyramid, interval is wider for each line
            if (j > height - i and j < height + i):
                # Get correct output, slice only last character
                output = str(j - height + i)[-1]
                print(output, end="")
            else:
                print(" ", end="")
        print()

def cross(size, center_value):
    for i in range(size):
        for j in range(size):
            # Print only on cross - vertical or horizontal middle
            if (i == size//2 or j == size//2):
                # y_addition provides proper change of vertical values of cross
                # x_addition will be used only if middle row is printed (otherwise its value is 0)
                y_addition = abs(i - size//2)
                x_addition = abs(j - size//2)
                # Slice only last character to ensure centering of cross
                output = str(center_value + y_addition + x_addition)[-1]
                print(output, end="")
            else:
                print(" ", end="")
        print()

def X(height, first_character):
    # Ensure that (first_character - i) will be always greater than 0 - used in for cycle
    first_character += math.ceil(height / 10) * 10
    for i in range(height):
        for j in range(height):
            if j == i or j == height - 1 - i:
                output = str(first_character - i)[-1]
                print(output, end="")
            else:
                print(" ", end="")
        print()

def honeycomb(n):
    painter = Turtle()
    for i in range(6):
        # Draw hexagon
        for j in range(6):
            painter.forward(n)
            painter.left(60)
        # Preparing for next iteration (get turtle to correct position)
        painter.forward(n)
        painter.right(60)
