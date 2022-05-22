from matplotlib import pyplot as plt
import numpy as np
EPS = 10 ** (-4)
l = 10
T0 = 300
R = 0.5
F0 = 50
a1 = 0.0134
b1 = 1
c1 = 4.35 * 10 ** (-4)
m1 = 1
alpha0 = 1.94 * 10 ** (-2)
delta = 1.5 * 10 ** 3
gamma = 0.2 * 10 ** (-2)
N = 100

h = l / N
# коэффиценты почти СЛАУ
A = [0 for _ in range(N + 1)]
B = [0 for _ in range(N + 1)]
C = [0 for _ in range(N + 1)]
D = [0 for _ in range(N + 1)]
# Линеаризация коэффициентов
A_ = [0 for _ in range(N + 1)]
B_ = [0 for _ in range(N + 1)]
C_ = [0 for _ in range(N + 1)]
D_ = [0 for _ in range(N + 1)]
# Коэффициенты для метода прогонки
ksi = [0 for _ in range(N + 1)]
teta = [0 for _ in range(N + 1)]
#
k = [0 for _ in range(N + 1)]
p = [0 for _ in range(N + 1)]
alpha = [0 for _ in range(N + 1)]
f = [0 for _ in range(N + 1)]
# T - значения температуры
T = [T0 for _ in range(N + 1)]

# функция нахождения p(T)
def func_p(T):
    return 2 / R * func_alpha(T)

# функция нахождения k(T)
def func_k(T):
    return a1 * (b1 + c1 * T**m1)

# функция нахождения f(T)
def func_f(T):
    return 2 * T0 / R * func_alpha(T)

# функция нахождения a(T)
def func_alpha(T):
    return alpha0 * (T / delta - 1) ** 4 + gamma

# функция нахождения k`(T)
def func_derv_k(T):
    return a1 * c1 * m1 * T**(m1-1)

# функция нахождения p`(T)
def func_derv_p(T):
    return 2 / R * func_derv_alpha(T)

# функция нахождения f`(T)
def func_derv_f(T):
    return 2 * T0 / R * func_derv_alpha(T)

# функция нахождения a`(T)
def func_derv_alpha(T):
    return (4 * alpha0 * (T / delta - 1)**3) / delta


xBorders = [0, l]
print("h =", h)
xValues = np.arange(0, l + h, h)
print("xValues =", xValues)

# K[i + 1/2]
def K_plus(x, i):
    return (k[i] + k[i + 1]) / 2

# K[i - 1/2]
def K_minus(k, i):
    return (k[i - 1] + k[i]) / 2

max_dy = 1
while max_dy > EPS:
    for i in range(N + 1):
        # нахождение k, a, p, f
        k[i] = func_k(T[i])
        alpha[i] = func_alpha(T[i])
        p[i] = func_p(T[i])
        f[i] = func_f(T[i])

        # Крайвой случай F(x0)
        if i == 0:
            k[1] = func_k(T[1])

            A[0] = 0
            B[0] = K_plus(k, 0) + p[0] * h**2
            C[0] = K_plus(k, 0)
            D[0] = f[0] * h**2 + F0 * h

            Aderv = 0
            Bderv = lambda T: func_derv_k(T) / 2 + func_derv_p(T) * h**2
            Cderv = lambda T: func_derv_k(T) / 2
            Dderv = lambda T: func_derv_f(T) * h**2

            A_[0] = 0
            B_[0] = Bderv(T[i]) * T[i] + B[i] - Cderv(T[i]) * T[i + 1] - Dderv(T[i])
            C_[0] = -Cderv(T[i + 1]) * T[i] + Cderv(T[i + 1]) * T[i + 1]  + C[i]
            D_[0] = -B[i] * T[i] + C[i] * T[i + 1] + D[i]
            # print("A_new[0] = ", A_[0])
            # print("B_new[0] = ", B_[0])
            # print("C_new[0] = ", C_[0])
            # print("D_new[0] = ", D_[0])

        # Крайвой случай F(xN)
        elif i == N:
            A[N] = K_minus(k, N)
            B[N] = K_minus(k, N) + p[N] * h**2 + alpha[N] * h
            C[N] = 0.0
            D[N] = f[N] * h**2 + alpha[N] * T0 * h

            Aderv = lambda T: func_derv_k(T) / 2
            Bderv = lambda T: func_derv_k(T) / 2 + func_derv_p(T) * h**2 + func_derv_alpha(T) * h
            Cderv = 0.0
            Dderv = lambda T: func_derv_f(T) * h**2 + func_derv_alpha(T) * T0 * h

            A_[N] = Aderv(T[i - 1])  * T[i - 1] + A[i] - Aderv(T[i - 1]) * T[i]
            B_[N] = - Aderv(T[i]) * T[i - 1] + Bderv(T[i]) * T[i] + B[i] - Dderv(T[i])
            C_[N] = 0.0
            D_[N] = A[i] * T[i - 1] - B[i] * T[i] + D[i]
            # print("\nA_new[N] = ", A_[i])
            # print("B_new[N] = ", B_[i])
            # print("C_new[N] = ", C_[i])
            # print("D_new[N] = ", D_[i])

        # все остальные случае, то есть что от 0 до N
        else:
            k[i + 1] = func_k(T[i + 1])

            A[i] = K_minus(k, i)
            B[i] = K_minus(k, i) +  K_plus(k, i) + p[i] * h**2
            C[i] = K_plus(k, i)
            D[i] = f[i] * h**2

            Aderv = lambda T: func_derv_k(T) / 2
            Bderv = lambda T: func_derv_k(T) + func_derv_p(T) * h ** 2
            Cderv = lambda T: func_derv_k(T) / 2
            Dderv = lambda T: func_derv_f(T) * h ** 2

            A_[i] = Aderv(T[i - 1]) * T[i - 1] + A[i] - Aderv(T[i - 1]) * T[i]
            B_[i] = -Aderv(T[i]) * T[i - 1] + Bderv(T[i]) * T[i] + B[i] - Cderv(T[i]) * T[i + 1] - Dderv(T[i])
            C_[i] = -Cderv(T[i + 1]) * T[i] + Cderv(T[i + 1]) * T[i + 1] + C[i]
            D_[i] = A[i] * T[i - 1] - B[i] * T[i] + C[i] * T[i + 1] + D[i]
            # print("\nA_new[i] = ", A_[i])
            # print("B_new[i] = ", B_[i])
            # print("C_new[i] = ", C_[i])
            # print("D_new[i] = ", D_[i])

        if i > 0:
            ksi[i] = C_[i - 1] / (B_[i - 1] - A_[i - 1] * ksi[i - 1])
            teta[i] = (A_[i - 1] * teta[i - 1] + D_[i - 1]) / (B_[i - 1] - A_[i - 1] * ksi[i - 1])


    dy = [0 for _ in range(N + 1)]
    max_dy = 0

    for i in range(N, -1, -1):
        if i < N:
            dy[i] = ksi[i + 1] * dy[i + 1] + teta[i + 1]
        else:
            dy[i] = (A_[i] * teta[i] + D_[i]) / (B_[i] - A_[i] * ksi[i])
        if T[i] != 0:
            max_dy = max(max_dy, abs(dy[i] / T[i]))
        else:
            max_dy = max(max_dy, 0)

    if max_dy > EPS:
        for i in range(N + 1):
            T[i] += dy[i]

fig, ax = plt.subplots()
text = "Зависимость температуры от расстояния от левого торца стержня T(x)."
print("k", k)
print("a", alpha)
print("p", p)
print("f", f)
print("T", T)

# print("------------maybe Slau--------------")
# for i in range (N + 1):
#     print(str(i + 1) + ") " +str(round(A[i],4)) + "*y_i-1 - " +
#           str(round(B[i],4)) + "*y_i + " +
#           str(round(C[i],4)) + "*y_i+1 + " +
#           str(round(D[i],4)) + " = 0")
# print()
# print("-----------ToLinaer Slau-------------")
# for i in range (N + 1):
#     print(str(i + 1) + ") " +str(round(A_[i],4)) + "*dy_i-1 - " +
#           str(round(B_[i],4)) + "*dy_i + " +
#           str(round(C_[i],4)) + "*dy_i+1 + " +
#           str(round(D_[i],4)) + " = 0")

plt.title(text)
ax.plot(xValues, T, '-')
ax.set_xlabel('Расстояние от левого торца стержня, см')
ax.set_ylabel('Температура, К')
ax.grid(True)
plt.show()