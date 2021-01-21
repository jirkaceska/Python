from PIL import Image
from math import pi, sin, cos, acos


class SvgFile:
    def __init__(self, name):
        self.__file = open(name + ".svg", 'w')

    def __enter__(self):
        self.__file.write("<svg xmlns='http://www.w3.org/2000/svg'>")
        return self.__file

    def __exit__(self, type, value, traceback):
        self.__file.write('</svg>')
        self.__file.close()


class Turtle:
    def __init__(self, file, color="black", start=(500, 700)):
        self.__svg_file = file
        self._position = start
        self.__rotation = 0
        self._tracked = None
        self.__color = color

    def get_position(self):
        return self._position

    def add_tracked_turtle(self, turtle):
        self._tracked = turtle

    def line(self, start, end):
        self.__svg_file.write("<line x1='" + str(start[0]) + "' y1='" + str(start[1]) +
                              "' x2='" + str(end[0]) + "' y2='" + str(end[1]) +
                              "' stroke='" + self.__color + "' stroke-width='1'/>"
                              )

    def forward(self, length):
        alpha = self.__rotation / 180 * pi
        old_position = self._position
        self._position = (old_position[0] + cos(alpha) * length, old_position[1] + sin(alpha) * length)
        self.line(old_position, self._position)

    def left(self, angle):
        self.__rotation = (self.__rotation - angle) % 360

    def right(self, angle):
        self.__rotation = (self.__rotation + angle) % 360

    def turn_to_tracked(self):
        if self._tracked:
            tracked_pos = self._tracked.get_position()
            if tracked_pos != self._position:
                dx = tracked_pos[0] - self._position[0]
                dy = self._position[1] - tracked_pos[1]
                hypotenuse = (dx ** 2 + dy ** 2) ** (1 / 2)
                self.__rotation = ((1 if dy < pi else - 1) * acos(dx / hypotenuse) / pi * 180) % 360

    def draw_connection(self):
        tracked_pos = self._tracked.get_position()
        self.line(self._position, tracked_pos)


def two_on_circle(density=180, multiple=2):
    """
    Divide evenly circle to {density} points, then connect each point with its {multiple}
    E.g. 1 with 2, 2 with 4, 3 with 6 and so on
    """
    with SvgFile("svg_test") as svg_file:
        leading = Turtle(svg_file, "white")
        following = Turtle(svg_file, "red")

        following.add_tracked_turtle(leading)

        angle = 360 / density
        length = 5 * angle

        for _ in range(density):
            for _ in range(multiple):
                leading.forward(length)
                leading.left(angle)
            following.forward(length)
            following.left(angle)
            following.draw_connection()


def one_following_another():
    """
    First turtle follow circle, the other follow the first turtle and draw connection after every movement
    Both turtles start at different positions
    """
    with SvgFile("svg_test") as svg_file:
        leading = Turtle(svg_file, "white")
        following = Turtle(svg_file, "red")
        following.add_tracked_turtle(leading)

        for _ in range(720):
            for _ in range(2):
                leading.forward(6)
                leading.left(1)
            following.turn_to_tracked()
            following.forward(9)
            following.draw_connection()


# Choose function two_on_circle or one_following_another to get desired output
two_on_circle(369, 37)
# one_following_another()
