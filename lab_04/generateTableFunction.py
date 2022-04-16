import numpy as np
from pointClass import Point
from random import randint, random

def generateTable_1D(f, sx, ex, amount):
    dataTable = list()
    Xvalues = np.linspace(sx, ex, amount + 1)

    for x in Xvalues:
        dataTable.append(Point(x, f(x), 0, randint(1, 5)))

    return dataTable

def generateTable_2D(f, sx, ex, sy, ey, amount):
    dataTable = list()
    Xvalues = np.linspace(sx, ex, amount + 1)
    Yvalues = np.linspace(sy, ey, amount + 1)

    for i in range(amount):
        for j in range(amount):
            dataTable.append(Point(Xvalues[i], Yvalues[j], f(Xvalues[i], Yvalues[j]), randint(1, 10)))

    return dataTable