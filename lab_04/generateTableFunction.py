import numpy as np
from pointClass import Point
from random import randint, random

def generateTable_1D(f, sx, ex, amount):
    dataTable = list()
    Xvalues = np.linspace(sx, ex, amount + 1)

    for x in Xvalues:
        dataTable.append(Point(x, f(x), 0, randint(1, 5)))

    return dataTable

def generateTable_2D(f, sx, ex, sy, ey, amountX, amountY):
    dataTable = list()
    Xvalues = np.linspace(sx, ex, amountX)
    Yvalues = np.linspace(sy, ey, amountY)

    for i in range(amountX):
        for j in range(amountY):
            dataTable.append(Point(Xvalues[i], Yvalues[j], f(Xvalues[i], Yvalues[j]), randint(1, 10)))

    return dataTable