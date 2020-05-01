import os
from decimal import Decimal


class Storage(object):
    _map = {}

    def _put(self, key, value):
        self._map[key] = value

    def put(self, **kwargs):
        # print(kwargs)
        for key, value in kwargs.items():
            if isinstance(value, float):
                # value = round(value, 2)
                temp = value - int(value)
                value = int(value) + Decimal('{:g}'.format(Decimal('{:.{p}g}'.format(temp, p=2))))
            self._put(key, str(value))

    def pop(self, key):
        return self._map.pop(key, None)

    def export(self, filename):
        assert filename != ''
        with open(filename, 'w', encoding='utf8') as file:
            import json
            json.dump(self._map, file, indent=4, ensure_ascii=False)
        # self.append_tex_labels("latex/work.tex")

    # def append_tex_labels(self, filename):
    #     s = ''.join(['\label{%s}' % key for key, value in self._map.items() ])
    #     f = open(filename, "r")
    #     lines = f.read().splitlines()
    #     lines[-1] = s
    #     # f.write('\n'.join(lines))
    #     f.close()
    #     f = open(filename, "w")
    #     f.write('\n'.join(lines))
    #     f.close()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Storage, cls).__new__(cls)
        return cls.instance

