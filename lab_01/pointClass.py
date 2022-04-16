class Point:
    def __init__(self, x, y, derivative):
        self.x = x
        self.y = y
        self.derivative = derivative
        self.isExit = True

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getDerivative(self):
        return self.derivative

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.x = y

    def setDerivative(self, derivative):
        self.derivative = derivative