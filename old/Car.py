import pygame
from math import sin, cos, pi

TWO_PI = pi * 2
HALF_PI = pi / 2


def add_vectors(u, v):
    return (u[0] + v[0], u[1] + v[1])

def sub_vectors(u, v):
    return (u[0] - v[0], u[1] - v[1])

def midpoint(A, B):
    return (A[0]+B[0])/2, (A[1]+B[1])/2


class Car:

    # the neural network will control the angle and whether the car is moving or not

    def __init__(self, x, y, width, height, color=(255, 0, 0)):
        self.x, self.y = x, y # x, y: center
        self.width, self.height = width, height
        self.color = color
        self.angle = 0
        self.speed = 10
        self.rotate_speed = 0.2

    def move(self):
        self.x += self.speed * cos(self.angle)
        self.y += self.speed * sin(self.angle)

    def rotate_ccw(self):
        self.angle += self.rotate_speed

    def rotate_cw(self):
        self.angle -= self.rotate_speed

    def calculate_vertices(self):
        x_vec = (self.width / 2 * cos(self.angle), self.width / 2 * sin(self.angle))
        y_vec = (self.height / 2 * cos(self.angle + HALF_PI), self.height / 2 * sin(self.angle + HALF_PI))
        pos = (self.x, self.y)
        
        self.vertices = [
            add_vectors(sub_vectors(pos, x_vec), y_vec),
            sub_vectors(sub_vectors(pos, x_vec), y_vec),
            sub_vectors(add_vectors(pos, x_vec), y_vec),
            add_vectors(add_vectors(pos, x_vec), y_vec),
        ]

    def draw(self, win):
        pygame.draw.polygon(win, self.color, self.vertices)
        pygame.draw.line(win, (0, 0, 0), (self.x, self.y), midpoint(*self.vertices[2:4]))

    def update(self, win):
        self.angle %= TWO_PI
        self.calculate_vertices()
        self.draw(win)
