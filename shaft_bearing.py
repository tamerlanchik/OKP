import math

from latex_storage import Storage


def calcMinDiameter(M, d1, d2, shaft):
    F_circ1, F_circ2 = M/(d1/2), M/(d2/2)
    F_r1, F_r2 = F_circ1*math.tan(math.radians(20)), F_circ2*math.tan(math.radians(20))

    R_B_y = (shaft['g2']*F_r2 - shaft['g1']*F_r1)/shaft['L']
    R_A_y = F_r2 - F_r1 - R_B_y

    R_B_x = (shaft['g2']*F_circ2 + shaft['g1']*F_circ1)/shaft['L']
    R_A_x = F_circ1 + F_circ2 - R_B_x


    Mkx, Mky = 91.36, 24.3
    Msum_izg = math.sqrt(Mkx**2 + Mky**2)
    M_pr = math.sqrt(Msum_izg**2 + 0.75*M**2)

    d_min = (M_pr/(0.1*0.1*shaft['material']['sigma_b']))** (1.0/3)
    d_min_round = int(d_min+1)

    n = 218
    F_r_A = math.sqrt(R_A_x**2 + R_A_y**2)
    F_r_B = math.sqrt(R_B_x**2 + R_B_y**2)

    F_R = max(F_r_A, F_r_B)
    P = 1 * 1.2 * 1 * F_R
    Cp = 0.01 * P * (60*n*3000)**(1.0/3)

    tmpl = 'shaft.%s'
    damp = locals()
    Storage().put(**dict((tmpl % name, damp[name]) for name in (
        'M', 'F_circ1', 'F_circ2', 'F_r1', 'F_r2', 'R_B_x', 'R_B_y', 'R_A_x', 'R_A_y', 'Mkx', 'Mky', 'Msum_izg', 'M_pr', 'd_min', 'd_min_round',
        'P', 'F_R', 'F_r_A', 'F_r_B', 'n', 'Cp'
    )))