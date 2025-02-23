from typing import Tuple
import math
import random


class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.vector = [x, y]

    def __add__(self, other):
        return Vector2(self.vector[0] + other.vector[0], self.vector[1] + other.vector[1])

    def __sub__(self, other):
        return Vector2(self.vector[0] - other.vector[0], self.vector[1] - other.vector[1])

    def __mul__(self, scalar):
        return Vector2(self.vector[0] * scalar, self.vector[1] * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.vector[0] / scalar, self.vector[1] / scalar)

    def dot(self, other):
        return self.vector[0] * other.vector[0] + self.vector[1] * other.vector[1]

    def magnitude(self) -> float:
        return math.sqrt(self.vector[0] ** 2 + self.vector[1] ** 2)

    def magnitudeSquared(self) -> float:
        return self.vector[0] ** 2 + self.vector[1] ** 2

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2()
        inv_mag = 1.0 / mag
        return self*inv_mag

    def __repr__(self):
        return f"Vector2({self.vector[0]}, {self.vector[1]})"

    def __getitem__(self, index):
        return self.vector[index]

    @property
    def x(self):
        return self.vector[0]

    @x.setter
    def x(self, value):
        self.vector[0] = value

    @property
    def y(self):
        return self.vector[1]

    @y.setter
    def y(self, value):
        self.vector[1] = value


def approx_sqrt(x: float) -> float:
    if x <= 0:
        return 0
    guess = x
    # Perform one iteration of Newton's method
    guess = 0.5 * (guess + x / guess)
    return guess


class Particle:
    def __init__(self, x, y):
        self.position: Vector2 = Vector2(x, y)
        self.prevPosition: Vector2 = Vector2(x, y)
        self.velocity = Vector2(random.uniform(
            -0.2, 0.2), random.uniform(-0.2, 0.2))
        self.colour = (50, 80, 255)
