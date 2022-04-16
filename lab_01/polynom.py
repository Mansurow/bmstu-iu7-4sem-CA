import numpy as numpy
from pointClass import *

notMonotone = 'notMonotone'
increasing = 'increasing'
decreasing = 'decreasing'


def getTypeOfMonotone(pointTable):
    isIncreasing = True
    isDecreasing = True
    for rowI in range(len(pointTable) - 1):
        if not (pointTable[rowI].x < pointTable[rowI + 1].x and pointTable[rowI].x < pointTable[rowI + 1].x):
            isIncreasing = False
    for rowI in range(len(pointTable) - 1):
        if not (pointTable[rowI].x > pointTable[rowI + 1].x and pointTable[rowI].x > pointTable[rowI + 1].x):
            isDecreasing = False
    if isIncreasing:
        return increasing
    if isDecreasing:
        return decreasing
    return notMonotone


def getIndex(points, x):
    dif = abs(points[0].x - x)
    index = 0
    for i in range(len(points)):
        if abs(points[i].x - x) < dif:
            dif = abs(points[i].x - x)
            index = i
    return index


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
            cur = (curYRow[j] - curYRow[j + 1]) / (XRow[j] - XRow[j + countOfArgs])
            tableOfSub[countOfArgs + countOfRowsOfTableData - 1].append(cur)
    return tableOfSub


def calcApproximateValue(tableOfSub, n, x):
    countOfArgs = 2
    sum = tableOfSub[1][0]
    mainPart = 1
    for i in range(n):
        mainPart *= (x - tableOfSub[0][i])
        sum += mainPart * tableOfSub[i + countOfArgs][0]
    return sum


def HermitMethod(pointTable):
    countOfRowsOfTableData = 2
    tableOfSub = []
    [tableOfSub.append([point.x, point.y]) for point in pointTable]
    YdRow = []
    for point in pointTable:
        YdRow.append(point.derivative)
        YdRow.append(None)
    XColId = 0
    YColId = 1
    # Вставка пустых списком (будущих разностей) в 3 столбец
    for i in range(0, len(tableOfSub) * 2, 2): tableOfSub.insert(i + 1, [])
    # Копирование точек
    for i in range(0, len(tableOfSub), 2):
        tableOfSub[i + 1].append(tableOfSub[i][XColId])
        tableOfSub[i + 1].append(tableOfSub[i][YColId])
    for i in range(0, len(tableOfSub) - 2, 2):
        subElement = (tableOfSub[i][YColId] - tableOfSub[i + 2][YColId]) / (tableOfSub[i][XColId] - tableOfSub[i + 2][XColId])
        # if not pointTable[i + 1].isExit:
        #     continue
        # else:
        YdRow[i + 1] = subElement
    tableOfSub = list([list(row) for row in numpy.transpose(tableOfSub)])
    XRow = tableOfSub[0]
    YdRow.pop()
    tableOfSub.append(YdRow)

    # Добавление столбцов (строк в моей реализации)
    for countOfArgs in range(2, len(XRow)):
        tableOfSub.append([])
        curYRow = tableOfSub[len(tableOfSub) - countOfRowsOfTableData]
        # Добавление очередного элемента
        for j in range(0, len(XRow) - countOfArgs):
            if (abs(XRow[j] - XRow[j + countOfArgs]) < 1e-8):
                cur = YdRow[j]
            else:
                cur = (curYRow[j] - curYRow[j + 1]) / (XRow[j] - XRow[j + countOfArgs])
            tableOfSub[countOfArgs + countOfRowsOfTableData - 1].append(cur)
    # Удаление пустого списка
    return tableOfSub


def calcApproximateValue(tableOfSub, n, x):
    countOfArgs = 2
    sum = tableOfSub[1][0]
    mainPart = 1
    # print('N ',n)
    for i in range(n):
        mainPart *= (x - tableOfSub[0][i])
        sum += mainPart * tableOfSub[i + countOfArgs][0]
        # print("value", tableOfSub[i + countOfArgs][0])
    return sum


def rootByNewton(pointTable, n, monotone):
    newTable = []
    if monotone != notMonotone:
        for point in pointTable:
            newTable.append(Point(point.y, point.x, 0))
        newTable.sort(key=lambda point: point.x)
        subs = NewtonMethod(newTable)
        return calcApproximateValue(subs, n, 0)
    else:
        subs = NewtonMethod(pointTable)
        r = pointTable[-1].x
        l = pointTable[0].x
        while r - l > 1e-8:
            m = (r + l) / 2
            y = calcApproximateValue(subs, n, m)
            if y < 0:
                l = m
            else:
                r = m
        return l


def rootByHermit(pointTable, n, monotone):
    if monotone != notMonotone:
        newTable = []
        for i in pointTable:
            if i.derivative != 0:
                newTable.append(Point(i.y, i.x, 1 / i.derivative))
            else:
                p = Point(i.y, i.x, 0)
                p.isExit = False
                newTable.append(p)
        newTable.sort(key=lambda point: point.x)
        subs = HermitMethod(newTable)
        return calcApproximateValue(subs, n, 0)
    else:
        tableOfSub = HermitMethod(pointTable)
        r = pointTable[-1].x
        l = pointTable[0].x
        while r - l > 1e-8:
            m = (r + l) / 2
            y = calcApproximateValue(tableOfSub, n, m)
            if y < 0:
                l = m
            else:
                r = m
        return l


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