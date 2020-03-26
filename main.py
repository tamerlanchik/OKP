from engine import *
from input import *
from p1 import *

minEngineN, Mout = CalculatEnginePower(input_params['w_out'],
                                input_params['e_out'],
                                input_params['J_load'],
                                 xi=1.1,
                                 kpd_red=0.8)
assert minEngineN < engine['N']

materials = InflateMaterials(materials)
i0 = CalculateTotalGearRatio(engine['n'], input_params['w_out'])

res, momN, momE = CheckEngineWithMoments(engine, input_params['e_out'], input_params['J_load'], i0, 1.1)
if res == True:
    print("\033[32mПроверка двигателя по моментам пройдена\033[0m")

else:
    print("\033[31mПроверка двигателя по моменту не пройдена:\nМомент нагрузки: %f\nМомент двигателя:%f\033[0m" % (momN, momE))
    exit(1)

i = CalculateGearRatios(i0)
shaftCount = len(i)
M = CalculateBaseMoments(i, Mout)

gear_z, _ = SupplementListWithLastValue(minZ, length=shaftCount)   #   минимальное ограничение на число зубьев - против слишком маленьких шестерней
# gear_z = [35]*shaftCount        #   минимальное ограничение на число зубьев - против слишком маленьких шестерней
Z = CalculateToothCount(i, gear_z)
m = CalculateModule(Z, M, materials, 1.3, Ybm)
# m_common = max(minModule, max(m))
# print("Принимаем одинаковый для всех модуль: m=%.1f" % m_common)
m = CorrectModules(m, minModule)

gearGeometry = CalculateGeometry(i, Z, m, Yf)
for j in range(len(m)):
    gearGeometry[j]['m'] = m[j]
PrintGears(gearGeometry)
if not (input_params['d_connect'] + output_shaft_margin < gearGeometry[-1]['d'][1]['df']):
    print("\033[31mНедостаточный диаметр выходного колеса")
    exit(1)
if not CheckHole(gearGeometry, input_params['d_connect']):
    exit(-11)



recalcM = CalculateKpdMoments(gearGeometry, M[-1], kpdOp)

res = CalculateContactStrength(gearGeometry, materials, [elem['M'] for elem in recalcM])


print("Recalculated moments with new KPD: ", "\n".join(map(str, recalcM)))
print("Old moments: ", M[::-1])

loft_wheel['z'], loft_wheel['m'], loft_wheel['M'] = gearGeometry[-1]['d'][1]['z'], gearGeometry[-1]['m'], recalcM[-1]['M']
print("Проверка люфтовыбирающего колеса")
res, s = CheckLoftWheel(loft_wheel)
print(s)
print(tools.coloredText('DEBUG', 'red'))
if not res:
    exit()


print("END")