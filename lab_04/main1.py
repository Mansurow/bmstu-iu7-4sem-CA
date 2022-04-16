from math import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random

from math import exp


def f_exp(x, y):
    return x**2 + y**2


def phi(x, k):
    return pow(x, k)


def create_table():
    N = 10
    x = np.arange(0, 10, 1)
    y = np.arange(0, 10, 1)
    x, y = np.meshgrid(x, y)
    print(x)
    print()
    print(y)

    z = f_exp(x, y)
    ro = np.zeros(N)
    for i in range(N):
        ro[i] = 1
    x = x.tolist()
    y = y.tolist()
    z = z.tolist()
    return x, y, z, ro, N


def matr_for_gauss(table, n, len):
    n += 1
    sum_x = []
    for i in range(n * 2):
        sum_xi = 0
        for j in range(len):
            sum_xi += table[j][0] ** i * table[j][2]
        sum_x.append(sum_xi)
    sum_x_y = []
    for i in range(n):
        sum_yi = 0
        for j in range(len):
            sum_yi += table[j][0] ** i * table[j][2] * table[j][1]
        sum_x_y.append(sum_yi)

    gmatr = []
    for i in range(n):
        gstr = []
        for j in range(n):
            gstr.append(sum_x[i + j])
        gstr.append(sum_x_y[i])
        gmatr.append(gstr)
    print("------------------------------")
    for i in gmatr:
        print(i)

    return gmatr


def gauss(gmatr, n):

    n += 1
    for i in range(n):
        for j in range(i + 1, n):
            k = -(gmatr[j][i] / gmatr[i][i])
            for l in range(i, n + 1):
                gmatr[j][l] += k * gmatr[i][l]

    a = [0 for i in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            gmatr[i][n] -= a[j] * gmatr[i][j]
        a[i] = gmatr[i][n] / gmatr[i][i]
    return a


def f(arrx, arra):
    rez = []
    for j in range(len(arrx)):
        rezi = 0
        for i in range(len(arra)):
            rezi += arra[i] * (arrx[j] ** i)
        rez.append(rezi)
    return rez


def third_step(table, n, lenn):
    arrx = np.arange(table[0][0], table[lenn - 1][0], 0.1)
    newy = []
    for i in range(lenn):
        newy.append(table[i][1])
    table_of_tables = []
    for i in range(lenn):
        new_t = []
        for j in range(lenn):
            new_t.append([table[j][0], table[i][2][j], table[j][3]])
        gmatr = matr_for_gauss(new_t, n, lenn)
        a = gauss(gmatr, n)
        table_of_tables.append(f(arrx, a))

    arra = []
    for i in range(arrx.size):
        tab_y = []
        for j in range(lenn):
            tab_y.append([newy[j], table_of_tables[j][i], table[j][3]])
        gmatr = matr_for_gauss(tab_y, n, lenn)
        a = gauss(gmatr, n)
        arra.append(a)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print(arra)
    return arra


def makeGraph(table, n, N):
    lenn = N
    xGraph = np.arange(table[0][0], table[lenn - 1][0], 0.1)
    yGraph = np.arange(table[0][1], table[lenn - 1][1], (table[lenn - 1][1] - table[0][1]) / len(xGraph))
    zGraph = np.zeros([xGraph.size, yGraph.size])
    arra = third_step(table, n, N)

    for i in range(xGraph.size):
        k = np.array(f(yGraph, arra[i]))
        for j in range(xGraph.size):
            zGraph[i][j] = k[j]
    xGraph, yGraph = np.meshgrid(xGraph, yGraph)
    return xGraph, yGraph, zGraph


def graphic(x, y, z, xGraph, yGraph, zGraph):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    surf = ax.plot_surface(yGraph, xGraph, zGraph)
    ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.5)
    plt.show()


def randran(n, vmin, vmax):
    return (vmax - vmin) * np.random.rand(n) + vmin


def main():
    x, y, z, ro, N = create_table()

    table = []
    for i in range(N):
        table.append([x[0][i], y[i][0], z[i], 1])
    n = int(input("Введите степень полинома: "))
    while (n <= 0 and n > 2):
        print("Степень полинома должна быть больше 0\n")
        n = int(input("Введите степень полинома: "))
    xGraph, yGraph, zGraph = makeGraph(table, n, N)
    graphic(x, y, z, xGraph, yGraph, zGraph)


if __name__ == "__main__":
    main()