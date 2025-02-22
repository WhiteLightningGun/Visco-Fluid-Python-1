from typing import Tuple

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
        return (self.x**2 + self.y**2)**0.5
    
    def magnitudeSquared(self) -> float:
        return (self.x**2 + self.y**2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2()
        return self / mag

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"



class Particle:
    def __init__(self, x,y):
        self.position: Vector2 = Vector2(x, y)
        self.prevPosition: Vector2 = Vector2(x, y)
        self.velocity = self.position*0.005
        self.colour = (50, 80, 255)

        