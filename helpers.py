from math import sin, cos
from numpy import exp
from random import randint


def pointlist_midpoint(points):
    x, y = 0, 0
    for point in points:
        x += point[0]
        y += point[1]
    return x / len(points), y / len(points)


def rotate_in_place(points, angle):
    center = pointlist_midpoint(points)
    c, s = cos(angle), sin(angle)
    for i, point in enumerate(points):
        points[i] = ((point[0] - center[0]) * c - (point[1] - center[1]) * s + center[0],
                     (point[0] - center[0]) * s + (point[1] - center[1]) * c + center[1])
    return points


def sigmoid(x):
    return 1 / (1 + exp(-x))


def random_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


def constrain(x, lower, upper):
    return min(upper, max(lower, x))
