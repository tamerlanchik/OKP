input_params = {
    'w_out': 5,         #   c^(-1)
    'e_out': 36,        #   c^(-2)
    'J_load': 0.015,    #   kgm^2
    'phi_out': 120,     #   \deg
    'd_connect': 50     #   mm
}

engine = {
    'name': 'ДГ-5ТА',
    'N': 5,             #   Вт
    'n': 6000,          #   об\мин
    'Mn': 10,           #   Н*мм
    'Mstart': 22,       #   Н*мм
    'Jr': 40*10**(-8),  #   кгм^2
    'D': 61,            #   мм
    'L': 142            #   мм
}

materials = {'wheel': {
        'name': 'сталь 45',
        'sigma_b': 580,     #   предел прочности
        'sigma_t': 360,     #   предел текучести
        'sigma_1': 203,     #   предел выносливости
        'sigma_f': 0,       #   изгибное напряжение
        'sigma_H': 0,       #   контактное напряжение
    },
    'gear': {
        'name': 'сталь 40Х',
        'sigma_b': 1000,     #   предел прочности
        'sigma_t': 830,     #   предел текучести
        'sigma_1': 430,
        'sigma_f': 0,       #   изгибное напряжение
        'sigma_H': 0,       #   контактное напряжение
    }
}

minModule = 0.5             #   влияем на общий диаметр колёс
output_shaft_margin = 10    #   запас на стенки вала и зубья для выходного колеса

# i = [1.51, 1.62, 2.63, 4.27, 4.58]

Yf = 8
M = [7, 10, 15, 39, 160, 520]    #   Н*мм
Ybm = 8
kpdOp = 0.98

eps_d = 2
eps_module = 1