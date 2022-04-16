from pointClass import *

def readFileTable(filename):
    dataTable = list()
    appr = 0
    try:
        file = open(filename)
        flag = 0
        for line in file.readlines():
            try:
                row = list(map(float, line.split("\t")))
            except:
                row = list(map(float, line.split(" ")))

            if flag == 0:
                l = len(row)
                flag = 1
                if l == 3:
                    appr = 1
                elif l == 4:
                    appr = 2
                else:
                    appr = -1
                    break

            if appr == 1:
                dataTable.append(Point(row[0], row[1], 0, row[2]))
            elif appr == 2:
                dataTable.append(Point(row[1], row[2], row[0], row[3]))
        file.close()
    except:
        appr = -1
    return dataTable, appr

# красивый вывод точки
def printTable_1D(pointTable):
    print("+" + "-" * 7 + ("+" + "-" * 12) * 3 + "+")
    print("| {:^5s} | {:^10s} | {:^10s} | {:^10s} |".format("№", "X", "Y", "Вес"))
    print("+" + "-" * 7 + ("+" + "-" * 12) * 3 + "+")
    for i in range(len(pointTable)):
        print("| {:^5d} | {:^10.3g} | {:^10.3g} | {:^10.3g} |".format(i + 1, pointTable[i].getX(), pointTable[i].getY(), pointTable[i].getWeight()))
    print("+" + "-" * 7 + ("+" + "-" * 12) * 3 + "+")

def printTable_2D(pointTable):
    print("+" + "-" * 7 + ("+" + "-" * 12) * 4 + "+")
    print("| {:^5s} | {:^10s} | {:^10s} | {:^10s} | {:^10s} |".format("№", "X", "Y", "Z", "Вес"))
    print("+" + "-" * 7 + ("+" + "-" * 12) * 4 + "+")
    for i in range(len(pointTable)):
        print("| {:^5d} | {:^10.3g} | {:^10.3g} | {:^10.3g} | {:^10.3g} |".format(i + 1, pointTable[i].getX(), pointTable[i].getY(), pointTable[i].getZ(), pointTable[i].getWeight()))
    print("+" + "-" * 7 + ("+" + "-" * 12) * 4 + "+")

def changeAllWeigth(pointTable):
    w = 1
    for p in pointTable:
     p.setWeight(w)

def changeWeigth(pointTable):
    answer = 0
    while answer == 0:
        index = int(input("Введите номер точки: "))
        if index <= 0 or index > len(pointTable):
            print(" Предупреждение! Такого номера точки нет!")
        else:
            w = 0
            while w < 1:
                w = int(input("Введите вес точки: "))
                if w < 1:
                    answer = 1
                else:
                    pointTable[index - 1].setWeight(w)

def inputApproximateDegree():
    n = -1
    while n < 0:
        n = int(input("Введите степень аппроксимации: "))
        if n < 0:
            print(" Предупреждение! Стпень аппроксимации не может быть меньше 0!")

    return n