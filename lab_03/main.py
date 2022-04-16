from polynom import *
from spline import *
from readData import *
import numpy as np
from matplotlib import pyplot as plt

#pointTable = readTable("./data.txt")
pointTable = generateTable(-10, 10, 11)
printTable(pointTable)

n = 3
x = float(input("Введите значение аргумента x: "))

start1 = 0
end1 = 0
start2 = 0
end2 = 0
start3 = 0
end3 = 0

yValues = [list(), list(), list(), list()]
if n < len(pointTable):
    print("Ньютон 3-й степени:         ", newtonPolynom(pointTable, n + 1, x))
    end2 = newtonPolynom(pointTable, n + 1, pointTable[-1].x)
    start3 = newtonPolynom(pointTable, n + 1, pointTable[0].x)
    end3 = newtonPolynom(pointTable, n + 1, pointTable[-1].x)
else:
    print("Ньютон 3-й степени нельзя посчитать стпени", n, ", так как точек всего", len(pointTable))

print("Cплайн 0 and 0:             ", spline(pointTable, x, start1, end1))
print("Cплайн 0 and P''(xn):       ", spline(pointTable, x, start2, end2))
print("Cплайн P''(x0) and P''(xn): ", spline(pointTable, x, start3, end3))

xValues = np.linspace(pointTable[0].x, pointTable[-1].x, 100)

if n < len(pointTable):
    for xi in xValues:
        yValues[3].append(newtonPolynom(pointTable, n + 1, xi))

for xi in xValues:
    yValues[0].append(spline(pointTable, xi, start1, end1))

for xi in xValues:
    yValues[1].append(spline(pointTable, xi, start2, end2))

for xi in xValues:
    yValues[2].append(spline(pointTable, xi, start3, end3))

plt.plot(xValues, yValues[0], '-', color='r')
plt.plot(xValues, yValues[1], '-', color='b')
plt.plot(xValues, yValues[2], '-', color='g')

if n < len(pointTable):
     plt.plot(xValues, yValues[3], ':', color='blue')

plt.show()