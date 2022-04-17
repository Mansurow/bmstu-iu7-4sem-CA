# x1 = xi-1
# x2 = xi
def H(x1, x2):
    return x2 - x1


# расчет коэффициента А
def A(x):
    return x


def C(c_i, ksi_i, teta_i):
    return ksi_i * c_i + teta_i


# расчет всех значений коэффициентов A
def calcAValues(yValues):
    AValues = list()
    for i in range(len(yValues) - 1):
        AValues.append(A(yValues[i]))
    return AValues
    # return yValues[:-1]


# y1 = yi-2
# y2 = yi-1
# y3 = yi
# h1 = hi-1
# h2 = hi
def fi(y1, y2, y3, h1, h2):
    return 3 * ((y3 - y2) / h2 - (y2 - y1) / h1)


# функция ksi - расcчтывает значение ksi i-го элемента
# ksi_i+1 = -h_i / (h_i-1  * ksi_i-1 * (h_i - h_i-1))
# ksi_i = -h_i-1 / (h_i  * ksi_i + 2 * (h_i-1 - h_i))
# ksi1 = ksi_i-1
# h1 = h_i-1
# h2 = h_i
def ksi(ksi1, h1, h2):
    return - h1 / (h2 * ksi1 + 2 * (h2 + h1))


# fi - значение из функции fi()
# teta - teta_i-1
# ksi - ksi_i-1
# h1 - h_i-1
# h2 - h_i
def teta(fi, teta_i, ksi_i, h1, h2):
    return (fi - h1 * teta_i) / (h1 * ksi_i + 2 * (h2 + h1))


def calcHValues(xValues):
    hValues = list()
    for i in range(1, len(xValues)):
        hValues.append(H(xValues[i], xValues[i - 1]))

    return hValues


def calcCValues(xValues, yValues, start, end):
    sizeX = len(xValues)

    cValues = [0] * (sizeX - 1)
    cValues[0] = start
    cValues[1] = end
    ksiValues = [start, end]
    tetaValues = [start, end]

    for i in range(2, sizeX):
        h2 = xValues[i] - xValues[i - 1]       # hi
        h1 = xValues[i - 1] - xValues[i - 2]   # hi-1

        fiCur = fi(yValues[i - 2], yValues[i - 1], yValues[i], h1, h2)
        ksiCur = ksi(ksiValues[i - 1], h1, h2)
        tetaCur = teta(fiCur, tetaValues[i - 1], ksiValues[i - 1], h1, h2)

        ksiValues.append(ksiCur)
        tetaValues.append(tetaCur)

    cValues[-1] = tetaValues[-1]

    for i in range(sizeX - 2, 0, -1):
        cValues[i - 1] = C(cValues[i], ksiValues[i], tetaValues[i])

    return cValues


# y1 = y_i-1
# y2 = y_i
# hi
# c1 = c_i+1
# c2 = c_i
def B(y1, y2, c1, c2, hi):
    return (y2 - y1) / hi - (hi * (c2 + 2 * c1) / 3)


def D(c1, c2, hi):
    return (c1 - c2) / (3 * hi)


def calcBValues(xValues, yValues, cValues):
    bValues = list()
    for i in range(1, len(xValues) - 1):
        hi = xValues[i] - xValues[i - 1]
        bValues.append(B(yValues[i - 1], yValues[i], cValues[i - 1], cValues[i], hi))

    hi = xValues[-1] - xValues[-2]
    bValues.append(B(yValues[-2], yValues[-1], 0, cValues[-1], hi))

    return bValues


def calcDValues(xValues, cValues):
    dValues = []

    size = len(xValues)

    for i in range(1, size - 1):
        hi = xValues[i] - xValues[i - 1]
        dValues.append(D(cValues[i], cValues[i - 1], hi))

    hi = xValues[-1] - xValues[-2]
    dValues.append(D(0, cValues[-1], hi))

    return dValues


def calculateCoefsSpline(xValues, yValues, start, end):
    aValues = calcAValues(yValues)
    cValues = calcCValues(xValues, yValues, start, end)
    bValues = calcBValues(xValues, yValues, cValues)
    dValues = calcDValues(xValues, cValues)

    return aValues, bValues, cValues, dValues


def finedIndex(xValues, x):
    size = len(xValues)
    index = 1

    while index < size and xValues[index] < x:
        index += 1

    return index - 1


def countPolynom(x, xValues, index, coefs):
    h = x - xValues[index]
    y = 0

    for i in range(4):
        y += coefs[i][index] * (h ** i)

    return y


def printSplineFunct(table, x, start, end):
    xValues = [i.getX() for i in table]
    yValues = [i.getY() for i in table]

    index = finedIndex(xValues, x)
    coeffs = calculateCoefsSpline(xValues, yValues, start, end)

    print("x = {:.6g}".format(x))

    print("Ф(x) = {:.6g}".format(coeffs[0][index]), end=" ")
    for i in range (1, len(coeffs)):
        print("+ {:.6f}".format(coeffs[i][index]), "* (x -", xValues[index], end=") ")

    y = countPolynom(x, xValues, index, coeffs)
    print("= {:.6f}".format(y))

def spline(table, x, start, end):
    xValues = [i.getX() for i in table]
    yValues = [i.getY() for i in table]

    coeffs = calculateCoefsSpline(xValues, yValues, start, end)

    index = finedIndex(xValues, x)

    y = countPolynom(x, xValues, index, coeffs)

    return y
