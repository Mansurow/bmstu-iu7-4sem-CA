import numpy as numpy
from pointClass import *

# константы для работы с массивом данных
xIndexData = 0 # индекс x
yIndexData = 1 # индекс y
zIndexData = 2 # индекс z
matrixIndexData = 3 # индекс матрицы
infinity = None

# нахождение индекса ближайшей точки по значению к искомой
def getIndex(points, x):
    dif = abs(points[0].x - x)
    index = 0
    for i in range(len(points)):
        if abs(points[i].x - x) < dif:
            dif = abs(points[i].x - x)
            index = i
    return index


# взятие рабочих ближайших точек для расчетов
def getWorkingPoints(points, index, n):
    left = index
    right = index
    for i in range(n - 1):
        if i % 2 == 0:
            if left == 0:
                right += 1
            else:
                left -= 1
        else:
            if right == len(points) - 1:
                left -= 1
            else:
                right += 1
    return points[left:right + 1]

# расчет полином Ньютона м результаты в виде таблицы всех данных f(xi .... xn)
def NewtonMethod(pointTable):
    countOfRowsOfTableData = 2
    tableOfSub = []
    [tableOfSub.append([point.x, point.y]) for point in pointTable]

    tableOfSub = list([list(row) for row in numpy.transpose(tableOfSub)])
    XRow = tableOfSub[0]
    # Добавление столбцов (строк в моей реализации)
    for countOfArgs in range(1, len(XRow)):
        tableOfSub.append([])
        curYRow = tableOfSub[len(tableOfSub) - countOfRowsOfTableData]
        # Добавление очередного элемента
        for j in range(0, len(XRow) - countOfArgs):
            if curYRow[j] == infinity and curYRow[j + 1] == infinity:
                cur = 1
            elif curYRow[j] == infinity:
                cur = curYRow[j + 1] / (XRow[j] - XRow[j + countOfArgs])
            elif curYRow[j + 1] == infinity:
                print(2)
                cur = curYRow[j] / (XRow[j] - XRow[j + countOfArgs])
            else:
                cur = (curYRow[j] - curYRow[j + 1]) / (XRow[j] - XRow[j + countOfArgs])
            tableOfSub[countOfArgs + countOfRowsOfTableData - 1].append(cur)
    return tableOfSub


# скомпликтовал в одну функцию
def newtonPolynom(pointTable, n, x):
    workingTable = getWorkingPoints(pointTable, getIndex(pointTable, x), n)
    subs = NewtonMethod(workingTable)
    # for i in subs:
    #     print(i)
    # print("---------------------")
    # printSubTable(subs)
    return calcApproximateValue(subs, n - 2, x)


# расчет конечного результат по польном Ньютону
def calcApproximateValue(tableOfSub, n, x):
    countOfArgs = 2

    if tableOfSub[1][0] == infinity:
        sum = tableOfSub[1][1]
    else:
        sum = tableOfSub[1][0]

    mainPart = 1
    for i in range(n):
        if tableOfSub[0][i] == infinity:
            mainPart *= x
        else:
            mainPart *= (x - tableOfSub[0][i])

        if tableOfSub[i + countOfArgs][0] != infinity:
            sum += mainPart * tableOfSub[i + countOfArgs][0]
    return sum


# вывод таблицу всех данных f(xi .... xn)
def printSubTable(subTable):
    countArray = len(subTable)
    maxLen = len(subTable[0])
    print(("+" + "-" * 22) * countArray + "+")
    print("| {:^20s} | {:^20s}".format("X", "Y"), end=' ')
    for k in range(2, countArray):
        print("| {:^20s}".format("Y" + "\'" * (k - 1)), end=' ')
    print("|")
    print(("+" + "-" * 22) * countArray + "+")

    for i in range(maxLen):
        for j in range(countArray):
            if j >= countArray - i:
                print("| {:^20s}".format(" "), end=' ')
            else:
                print("| {:^20.10f}".format(subTable[j][i]), end=' ')
        print("|")

    print(("+" + "-" * 22) * countArray + "+")


# расчет трехметрной интерполяции Полином Ньютона
def findMultidimensionalInterpolation(data, nx, ny, nz, xp, yp, zp):
    matrix = data[matrixIndexData]
    xArr = data[xIndexData]
    yArr = data[yIndexData]
    zArr = data[zIndexData]

    z_values = []
    for k in range(len(zArr)):
        y_values = []

        for i in range(len(yArr)):
            x_values = []

            for j in range(len(xArr)):
                x_values.append(Point(xArr[j], matrix[k][i][j]))
            # print("Значение для нахождение полином Ньютона nx: (x_values)")
            # for el in x_values:
            #     print(el.getX(), el.getY())
            # print("end\n")

            y_values.append(Point(yArr[i], newtonPolynom(x_values, nx, xp)))
        # print("Значение для нахождение полином Ньютона ny: (y_values)")
        # for el in y_values:
        #     print(el.getX(), el.getY())
        # print("end\n")

        z_values.append(Point(zArr[k], newtonPolynom(y_values, ny, yp)))

    # print("Значение для нахождение полином Ньютона nz: (z_values)")
    # for el in z_values:
    #     print(el.getX(), el.getY())
    # print("end\n")

    return newtonPolynom(z_values, nz, zp)