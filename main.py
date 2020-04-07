import calc_job
from latex_storage import Storage
from input import loft_wheel

def dump_data(storage, filename):
    storage.put(M_load=calc_job.Mout, N_min=calc_job.minEngineN)
    storage.put(**{'i0': calc_job.i0})
    storage.put(momE=calc_job.momE, momN=calc_job.momN)
    storage.put(**dict(('i%d-%d' % (j, j+1), calc_job.i[j]) for j in range(len(calc_job.i))))
    storage.put(**dict(('M%d'%j, calc_job.M[j]) for j in range(len(calc_job.M))))
    # пишем геометрический расчёт
    for i in range(len(calc_job.gearGeometry)):
        pair = calc_job.gearGeometry[i]
        for j in range(2):
            for key, value in pair['d'][j].items():
                storage.put(**{
                    'gears.%d.%s' % (i * 2 + j + 1, key): value
                })
        pref = 'gears.{0}.%s'.format(2*i+1)
        for key in ['b', 'a', 'i', 'm']:
            storage.put(**{
                pref % key: pair[key]
            })

    # пишем выбранную шестерню
    storage.put(**dict(
        ('spr.%s' % key, value) for key, value in loft_wheel['spring'].items()
    ))
    storage.put(text=0.123*10**(5))
    storage.export(filename)

dump_data(Storage(), 'latex/work.json')