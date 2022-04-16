from polynom import *
from readData import *

# чтение данных в представлении
# за 0 индексом хранятся значения абцисс x
# за 1 индексом хранятся заняения ординат y
# за 2 индексом хранятся значение z
# за 3 индексом хранится сам кубическая матрица


# # чтение из файла не знай саму функцию
# table = readTable("data.txt")
# # вывод кубической матрицы
# printTable(table)

# генерация данных по значению функции
# интервал -5 до 5 и количество узлов 5 также и в остальных
xstart, xend, xpoints = -5, 5, 20
ystart, yend, ypoints = -3, 4, 50
zstart, zend, zpoints = -1, 2, 30
#
table = generateTable(xstart, xend, xpoints,
                      ystart, yend, ypoints,
                      zstart, zend, zpoints)
# printTable(table)

# Ввод данных для расчетов
# аргументы
x = float(input("Введите аргумент x: "))
y = float(input("Введите аргумент y: "))
z = float(input("Введите аргумент z: "))
# Cтепени трехмерной интерполяции u = f(x, y, z)
nx = int(input("Введите степень аппроксимиляции nx: "))
ny = int(input("Введите степень аппроксимиляции ny: "))
nz = int(input("Введите степень аппроксимиляции nz: "))

print("Result:")
try:
    print("u = f(x, y, z) = {:.9f}".format(findMultidimensionalInterpolation(table, nx + 1, ny + 1, nz + 1, x, y, z)))
    # если таблица генеруется кодом
    print("Generation u = f(x, y, z) = {:.9f}\n".format(f(x, y, z)))
    #Вывод всеч возможной интерполяции с помощью полином Ньютона, Эрмита неиспользую, т.к. нет данных о производных
    print("All result:")
    for i_nz in range(1, nz + 1):
        print("nz =", i_nz)
        print("+" + "-" * 10 + ("+" + "-" * 10) * nx + "+")
        print("| {:^8s}".format("ny \\ nx"), end=" ")

        for i in range(1, nx + 1):
            print("| {:^8d}".format(i), end=" ")
        print("|")

        print("+" + "-" * 10 + ("+" + "-" * 10) * nx + "+")
        for i_ny in range(1, ny + 1):
            print("| {:^8d}".format(i_ny), end=" ")
            for i_nx in range(1, nx + 1):
                print("| {:^8.3f}".format(findMultidimensionalInterpolation(table, i_nx + 1, i_ny + 1, i_nz + 1, x, y, z)), end=" ")
            print("|")
        print("+" + "-" * 10 + ("+" + "-" * 10) * nx + "+")
except:
    print("u = f(x, y, z) = inf")


