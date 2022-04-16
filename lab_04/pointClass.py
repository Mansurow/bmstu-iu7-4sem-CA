from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    z: float
    weight: float # p

    def __init__(self, x, y, z, weight):
        self.x = x
        self.y = y
        self.z = z
        self.weight = weight

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def getWeight(self):
        return self.weight

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setZ(self, z):
        self.z = z

    def setWeight(self, weight):
        self.weight = weight