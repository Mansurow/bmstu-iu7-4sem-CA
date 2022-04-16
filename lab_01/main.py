import readTxtToPoints as read
from polynom import *

pointTable = read.readTable("./data.txt")
monotone = getTypeOfMonotone(pointTable)
pointTable.sort(key=lambda point: point.x)

read.printTable(pointTable)

x = float(input("Введите x: "))
n = int(input("Введите n: "))

index = getIndex(pointTable, x)
newPointTable = getWorkingPoints(pointTable, index, n + 1)
subsNewton = NewtonMethod(newPointTable)
subsHermit = HermitMethod(newPointTable)
print("Newton:")
printSubTable(subsNewton)
print("Hermit:")
printSubTable(subsHermit)

print("Newton: {:.6f}".format(calcApproximateValue(subsNewton, n, x)))
print("Hermit: {:.6f}".format(calcApproximateValue(subsHermit, n, x)))

print("Root by Newton: {:.6f}".format(rootByNewton(pointTable, n, monotone)))
print("Root by Hermit: {:.6f}".format(rootByHermit(pointTable, n, monotone)))
