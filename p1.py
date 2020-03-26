import tools
from input import *
from math import sqrt, log10, sin, cos, radians


def CalculateGearRatios(i0):
    n = int(round((3 + 1.85) / 2 * log10(i0), 0))
    i_avr = i0 ** (1. / n)
    assert n >= 5
    i = [0] * n

    i[0] = (2 * i_avr) ** (1. / 4)
    i[1] = sqrt(i_avr)

    i[-1] = i_avr ** 2 / i[0]
    i[-2] = i_avr ** 2 / i[1]

    for j in range(2, len(i) - 2):
        i[j] = i_avr
    return list(map(lambda v: round(v, 2), i))


def CalculateToothCount(iList, baseZ):
    Z = []
    for j in range(len(baseZ)):
        z1 = baseZ[j] * iList[j]
        Z.append(baseZ[j])
        Z.append(z1)
    return Z


def CalculateModule(Z, M, material, K, Ybm):
    YF = lambda x: 3.6 if (
                x > 80) else 6.39598364 - 0.22982 * x + 0.0082 * x ** 2 - 0.000155222 * x ** 3 + 1.5935909197769 * 10 ** (
        -6) * x ** 4 - 8.2802228698844 * 10 ** (-9) * x ** 5 + 1.6784912618852 * 10 ** (-11) * x ** 6
    m = []
    for i in range(len(M) - 1):
        z_gear = min(Z[2 * i], Z[2 * i + 1])
        z_wheel = max(Z[2 * i], Z[2 * i + 1])
        a = YF(z_gear) / material['gear']['sigma_f']
        b = YF(z_wheel) / material['wheel']['sigma_f']
        if a > b:
            yf = YF(YF(z_gear))
            sigma = material['gear']['sigma_f']
            z = z_gear
            print("Прочность по шестерне: Z=", z_gear)
        else:
            yf = YF(YF(z_wheel))
            sigma = material['wheel']['sigma_f']
            z = z_wheel
            print("Прочность по колесу: Z=", z_wheel)

        m_ = 1.4 * (
                M[i] * K * Yf / (Ybm * z * sigma)
        ) ** (1. / 3)
        m.append(round(m_, eps_module))
    print("Max module: %.2f" % max(m))
    return m


def CalculateGearDiam(z, m):
    if m <= 0.5:
        c = 0.5
    else:
        c = 0.35
    d = m * z
    da = 2 * m + d
    df = d - 2 * m * (1 + c)
    return {'d': round(d, eps_d), 'da': round(da, eps_d), 'df': round(df, eps_d), 'z': round(z, 0)}


def CalculateGeometry(i_, Z_, m_, Yf_):
    data = []
    for i in range(len(i_)):
        D = [CalculateGearDiam(Z_[2 * i], m_[i]), CalculateGearDiam(Z_[2 * i + 1], m_[i])]
        b = m_[i] * Yf_
        a = 0.5 * m_[i] * (Z_[2 * i] + Z_[2 * i + 1])
        dt = {'n': [2 * i + 1, 2 * i + 2], 'd': D, 'b': b, 'a': round(a, eps_d), 'i': i_[i], 'm': m_[i]}
        data.append(dt)
    return data


def CalculateKpdMoments(gG_, Min_, kpdOp):
    preM = Min_
    eps = 1.5
    f = 0.15

    buildStruct = lambda M, kpd: {'M': round(M, 2), 'Kpd': round(kpd, 2)}

    newM = [buildStruct(preM, 1)]

    for i in range(len(gG_) - 1, -1, -1):
        pair = gG_[i]
        g1, g2 = pair['d'][0], pair['d'][1]
        F = 2 * preM / (max(g1['d'], g2['d']))
        c = (F + 2.87) / (F + 0.17)
        kpd = 1 - 3.14 * c * eps * f * (1 / g1['z'] + 1 / g2['z'])
        preM = preM / (pair['i'] * kpd * kpdOp)
        newM.append(buildStruct(preM, kpd))

    return newM[::-1]


def CalculateBaseMoments(i_, Min_):
    M = [Min_] * (len(i_) + 1)
    mPre = Min_
    for i in range(len(i_) - 1, -1, -1):
        mPre /= (i_[i] * 0.98 * 0.99)
        M[i] = mPre
    return M


def PrintGears(gears):
    for gear in gears:
        print("%d-%d:\n" % (gear['n'][0], gear['n'][1]), gear['d'][0], "\n", gear['d'][1], "\n",
              "b=%.2f, a=%.2f, i=%.2f, m=%.1f" % (gear['b'], gear['a'], gear['i'], gear['m']))


def InflateMaterials(materials):
    n = 1.7  # запас прочности
    temp1, temp2 = materials['wheel']['sigma_1'], materials['gear']['sigma_1']
    materials['wheel']['sigma_1'] = 0.43 * materials['wheel']['sigma_b']
    materials['gear']['sigma_1'] = 0.35 * materials['gear']['sigma_b']
    materials['wheel']['sigma_f'] = materials['wheel']['sigma_1'] / n
    materials['gear']['sigma_f'] = materials['gear']['sigma_1'] / n

    materials['wheel']['sigma_H'] = 1.72 * materials['wheel']['sigma_1']
    materials['gear']['sigma_H'] = 1.72 * materials['gear']['sigma_1']
    return materials


#   Тищенко, с.68
def CalculateContactStrength(gears, materials, M):
    sigma_H = materials['wheel']['sigma_H']
    K = 1.2  # коэффициент расчётной нагрузки
    zk = 0.9  # для прямозубых передач
    for i in range(len(gears)):
        z1, z2 = gears[i]['d'][0]['z'], gears[i]['d'][1]['z']
        m, i0, b = gears[i]['m'], gears[i]['i'], gears[i]['b']
        a_w = (z1 + z2) * m / 2

        sigma_n = 108.5 * zk / (a_w * i0) * sqrt(
            (i0 + 1) ** 3 * K * M[i] / b
        )

        if sigma_n < sigma_H:
            print("Колесная пара %d: проверка на прочность пройдена: sigma_n=%d, [sigma_H]=%d" % (i, sigma_n, sigma_H))
        else:
            print(
                "Колесная пара %d: проверка на прочность НЕ пройдена: sigma_n=%d, [sigma_H]=%d" % (i, sigma_n, sigma_H))
            return False
    print("\033[32mРедуктор прошел проверку на прочность\033[0m")
    return True


def CorrectModules(current, constraints):
    current, constraints = SupplementListWithLastValue(current, constraints)
    return [max(current[i], constraints[i]) for i in range(len(current))]


# Приводит два массива к одному размеру
# путём дублирования последнего элемента
# меньшего массива
def SupplementListWithLastValue(a, b=[], length=0):
    destList, i = [], 0
    if b == []:
        destList, i = a, 0
    else:
        destList, i = (a, 0) if len(a) < len(b) else (b, 1)
    destLen = max(len(a), len(b), length)

    destList += [destList[-1]] * (destLen - len(destList))
    res = [a, b]
    res[i] = destList
    return res


def CheckHole(gears, dHole):
    pair = gears[-1]['d']
    surplus = (pair[0]['d'] + pair[1]['d']) / 2 - gears[-2]['d'][1]['da'] / 2 - dHole / 2
    if surplus > 0:
        print("\033[32mПроверка на свободное очко пройдена\033[0m")
        return True
    else:
        print("\033[31mПроверка на свободное очко НЕ пройдена: перекрытие %f мм\033[0m" % abs(surplus))
        return False


# Расчёт пружины для люфтовыбирающего колеса
#   :param int z - число зубьев рассчитываемого колеса
#   :param float m - модуль зуба
#   :param float M - крутящий момент на колесе
#   :param float xi - запас упругого момента
#   :param int L - начальная длина пружины
#   :param float A - расстояние от пружины до центра колеса
#   :param int n - относительное смеещение половин колеса, в зубьях
def LoshSpringCalculation(z: int, m: float, spinM: float, xi: float, L: int, A: float, n: int, delta: float):
    phi = radians(360 * n / z)                      # угол поворота одной половины колеса относительно другой
    A1 = A * cos(phi / 2) - L / 2 * sin(phi / 2)    # новое плечо действия пружины
    P2 = xi * spinM / (2 * A1)                      # жёсткость пружины
    P3 = P2 / (1 - delta)                           # максимальное усилие пружины
    return P3

def CheckLoftWheel(wheel):
    spring_strength = LoshSpringCalculation(
        z=wheel['z'], m=wheel['m'], spinM=wheel['M'], xi=wheel['xi'],
        L=wheel['spring']['L'], A=wheel['A'], n =4, delta=0.2,
    )
    if spring_strength > wheel['spring']['P3']:
        return False, \
               tools.coloredText('Пружина для люфтовыбирающего колеса слабая: %f > %f', 'red') \
               % (spring_strength, wheel['spring']['P3'])
    else:
        return True, \
                tools.coloredText('Пружина для люфтовыбирающего колеса годится: \n%s' % str(wheel))

def inflateLoftWheel(dest, z, m, M):
    dest['z'] = z
    dest['m'] = m
    dest['M'] = M