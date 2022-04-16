from pointClass import *
from math import fabs
import numpy as np
from matplotlib import pyplot as plt

#-----------------------------------------------------------------
def getIntervalX(table):
    minim = table[0].getX()
    maxim = table[0].getX()
    for p in table:
        value = p.getX()
        if value > maxim:
            maxim = value
        if value < minim:
            minim = value
    return minim, maxim

def getIntervalY(table):
    minim = table[0].getY()
    maxim = table[0].getY()
    for p in table:
        value = p.getY()
        if value > maxim:
            maxim = value
        if value < minim:
            minim = value
    return minim, maxim

def getIntervalZ(table):
    minim = table[0].getZ()
    maxim = table[0].getZ()
    for p in table:
        value = p.getZ()
        if value > maxim:
            maxim = value
        if value < minim:
            minim = value
    return minim, maxim
#-----------------------------------------------------------------

#-----------------------------------------------------------------
# Вывод коэффициентов a и СЛАУ
def printCoeff(coeffValues):
    print(":")
    for i in range(len(coeffValues)):
        print("a" + str(i) + " = {:10.6g}".format(coeffValues[i]))

def printMatrix(matrix):
    for row in matrix:
        for el in row:
            if fabs(el) < 1e-6:
                el = 0.0
            print("{:15.6g}".format(el), end=" ")
        print()
#-----------------------------------------------------------------

#-----------------------------------------------------------------
# Решение СЛАУ методом Гаусса
def toTriangleView(matrix):
    n = len(matrix)
    for k in range(n):
        for i in range(k + 1, n):
            coeff = -(matrix[i][k] / matrix[k][k])
            for j in range(k, n + 1):
                matrix[i][j] += coeff * matrix[k][j]

    return matrix

def Gauss(matrixSlau):
    n = len(matrixSlau)

    matrixSlau = toTriangleView(matrixSlau)

    print("\nМатрица преведена к треугольному ввиду:")
    printMatrix(matrixSlau)

    # находим неизвестные
    result = [0.0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            matrixSlau[i][n] -= result[j] * matrixSlau[i][j]

        result[i] = matrixSlau[i][n] / matrixSlau[i][i]
    return result
#-----------------------------------------------------------------

#-----------------------------------------------------------------
# Одномерная аппроксимация метод наименьших квадратов
def findAmountEquations_1D(n):
    return n + 1

def makeSlau_1D(pointTable, n):
    matrixSlau = [[0.0 for _ in range(n + 1)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            sums = 0
            for p  in pointTable:
                sums += p.getWeight() * p.getX()**(i + j)
            matrixSlau[i][j] = sums

        sums = 0
        for p in pointTable:
            sums += p.getWeight() * p.getY() * p.getX()**i
        matrixSlau[i][n] = sums

    return matrixSlau

def leastSquaresMethod_1D(pointTable, n=1):
    h = findAmountEquations_1D(n)
    slau = makeSlau_1D(pointTable, h)

    print("\nМатрица СЛАУ:")
    printMatrix(slau)
    aValues = Gauss(slau)

    printCoeff(aValues)

    def approximateFunction_1D(x):
        y = 0
        for i in range(len(aValues)):
            y += aValues[i] * x**i
        return y

    return approximateFunction_1D

def drawGraficBy_AproxFunction_1D(approximateFuction, pointTable):
    xMin, xMax = getIntervalX(pointTable)
    xValues = np.arange(xMin, xMax, 0.02)
    plt.figure("График функции, полученный аппроксимации наименьших квадратов")
    plt.ylabel("Y")
    plt.xlabel("X")
    for p in pointTable:
        plt.plot(p.getX(), p.getY(), 'r.')
    plt.plot(xValues, approximateFuction(xValues), 'k')
    plt.show()
#-----------------------------------------------------------------

#-----------------------------------------------------------------
# Двумерная аппроксимация метод наименьших квадратов
def findAmountEquations_2D(n):
    return int((n + 1) * (n + 2) / 2)

def makeSlau_2D(pointTable, n):
    a = list()
    b = list()
    for i in range(n + 1):
        for j in range(n + 1 - i):
            a_row = list()
            for k in range(n + 1):
                for t in range(n + 1 - k):
                    a_row.append(sum(
                        list(map(
                            lambda point: point.getX() ** (k + i) * point.getY() ** (t + j) * point.getWeight(),
                            pointTable
                        ))
                    ))
            a.append(a_row)
            b.append(
                sum(list(map(
                    lambda point: point.getX()**i * point.getY()**j * point.getZ() * point.getWeight(),
                    pointTable
                )))
            )

    slau = list()
    for i in range(len(a)):
        slau.append(a[i])
        slau[i].append(b[i])
    return slau

def leastSquaresMethod_2D(pointTable, n=1):

    slau = makeSlau_2D(pointTable, n)
    print("\nМатрица СЛАУ:")
    printMatrix(slau)
    # c = list(np.linalg.solve(a, b))
    aValues = Gauss(slau)
    printCoeff(aValues)

    def approximateFunction_2D(x, y):
        result = 0
        x_degree = 1
        a_index = 0
        for i in range(n + 1):
            y_degree = 1
            for _ in range(n + 1 - i):
                result += aValues[a_index] * x_degree * y_degree
                y_degree *= y
                a_index += 1
            x_degree *= x
        return result

    return approximateFunction_2D

def parseTableToCoordinates3D(pointTable):
    xs = list()
    ys = list()
    zs = list()
    for p in pointTable:
        xs.append(p.getX())
        ys.append(p.getY())
        zs.append(p.getZ())
    return np.array(xs), np.array(ys), np.array(zs)

def drawGraficBy_AproxFunction_2D(approximateFuction, pointTable, n):
    minX, maxX = getIntervalX(pointTable)
    minY, maxY = getIntervalY(pointTable)

    xValues = np.linspace(minX, maxX, 40)
    yValues = np.linspace(minY, maxY, 40)
    zValues = [approximateFuction(xValues[i], yValues[i]) for i in range(len(xValues))]

    def make_2D_matrix():
        # Создаем двумерную матрицу-сетку
        xGrid, yGrid = np.meshgrid(xValues, yValues)
        # В узлах рассчитываем значение функции
        zGrid = np.array([
            [
                approximateFuction(
                    xGrid[i][j],
                    yGrid[i][j],
                ) for j in range(len(xValues))
            ] for i in range(len(yValues))
        ])
        return xGrid, yGrid, zGrid

    fig = plt.figure("График функции, полученный аппроксимации наименьших квадратов")
    xpoints, ypoints, zpoints = parseTableToCoordinates3D(pointTable)
    axes = fig.add_subplot(projection='3d')
    axes.scatter(xpoints, ypoints, zpoints, c='red')
    axes.set_xlabel('X')
    axes.set_ylabel('Y')
    axes.set_zlabel('Z')
    xValues, yValues, zValues = make_2D_matrix()
    axes.plot_wireframe(xValues, yValues, zValues)
    plt.show()
#-----------------------------------------------------------------