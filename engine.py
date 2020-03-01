from math import log10
def CalculatEnginePower(w_out, e_out, J_out, xi, kpd_red):
    M_load = J_out*e_out            #   момент нагрузки
    N = xi*M_load*w_out/kpd_red     #   минимальная мощность двигла
    return N

def CheckEngineWithMoments(engine, e_out, J_out, i0, xi):
    Km = 0.5        # учитывает инерционность редуктора

    #   приведенная к валу динамическая нагрузка
    M_d_pr = e_out*i0 * (
        (1 + Km)*engine['Jr'] + J_out/(i0**2)
    ) * 10**3
    if engine['Mn'] > M_d_pr*xi:
        return (True, M_d_pr, engine['Mn'])
    else:
        return (False, M_d_pr, engine['Mn'])

def CalculateGearRatios(nEngine, wLoad):
    i0 = nEngine/(wLoad*30/3.14)

    # n = round((3 + 1.85)/2*log10(i0), 0)
    return round(i0, 0)
