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

def calcAccurance(wheels):
    j_n_max = [11, 11, 13, 16, 19]
    s = 0
    I_mul = [1] * len(wheels);
    for i in range(len(wheels)):

        for j in range(i, len(wheels)):
            I_mul[i] *= wheels[j]['i']
        Storage().put(**{
            "acc.I_mul.%d" % i: I_mul[i],
        })

        pair = wheels[i]
        m, z = pair['m'], pair['d'][0]['z']
        phi_L = 7.4*j_n_max[i]/(m*z)
        s += phi_L/I_mul[i]
        Storage().put(**{
            "acc.%d.phi_L" % i: phi_L,
        })
    Storage().put(**{
        "acc.phi_L": s,
    })

    F_f = [9]*8 + [10]*2
    F_p = [22, 24, 22, 24, 22, 30, 22, 35, 26, 42]
    Phi = []
    for i in range(len(wheels)):
        pair = wheels[i]
        m, z = pair['m'], pair['d'][0]['z']
        for j in range(2):
            phi = 4.8*(F_f[2*i+j] + F_p[2*i+j])/(m*z)
            Phi.append(phi)
            Storage().put(**{
                "acc.%d.phi_i" % (2*i+j + 1): phi,
            })
    phi_summ = Phi[0]/I_mul[0] + (Phi[1]+Phi[2])/I_mul[1] + (Phi[3]+Phi[4])/I_mul[2] + (Phi[5]+Phi[6])/I_mul[3] + (Phi[7]+Phi[8])/I_mul[4] + Phi[9]
    Storage().put(**{
        "acc.Phi":
            phi_summ,
        "acc.Sum": phi_summ + s,
    })




