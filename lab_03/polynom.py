import numpy as numpy
from pointClass import *

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
    return calcApproximateValue(subs, n, x)


# расчет конечного результат по польном Ньютону
def calcApproximateValue(tableOfSub, n, x):
    countOfArgs = 2

    if tableOfSub[1][0] == infinity:
        sum = tableOfSub[1][1]
    else:
        sum = tableOfSub[1][0]

    mainPart = 1

    for i in range(n - 1):
        if tableOfSub[0][i] == infinity:
            print(3)
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
