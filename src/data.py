from typing import Tuple
import math
import random


class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def magnitude(self) -> float:
        return math.sqrt((self.x**2 + self.y**2))

    def magnitudeSquared(self) -> float:
        return (self.x**2 + self.y**2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2()
        return self / mag

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"


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
