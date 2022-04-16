from pointClass import Point

def printFunction_1D(n):
    print("Функция линейной завизимостью вида: ")
    print("fi(x) = a0 ", end=" ")
    for i in range(1, n + 1):
        print("+ a" + str(i) + " * x^" + str(i), end=" ")
    print()

def printSlau_1D(n):
    print("Система линейных алгебраических уравнений (СЛАУ):")
    for i in range(n + 1):
        print(str(i + 1) + ") ", end="")
        for j in range(n + 1):
            if j != 0:
                print(" + ", end="")
            print("(x^" + str(i) + ", x^" + str(j) + ") * a" + str(j), end="")
        print(" = (y, x^" + str(i) + ")")


def printAboutSlauCoefficients_1D():
    print("Скалярные произведения в полученной системе записываются следующим образом:")
    print("             n")
    print("(x^a , x^b) = E pi * xi^(a + b)")
    print("            i=1")
    print("             n")
    print("(y , x^b) = E pi * yi * xi^b")
    print("            i=1")

