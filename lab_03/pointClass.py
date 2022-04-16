# ничего не буду объяснять принципы ООП
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.x = y

    def printData(self):
        print("[", self.x, self.y,  "]")