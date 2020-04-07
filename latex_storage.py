class Storage(object):
    _map = {}

    def _put(self, key, value):
        self._map[key] = value

    def put(self, **kwargs):
        # print(kwargs)
        for key, value in kwargs.items():
            if isinstance(value, float):
                value = round(value, 2)
            self._put(key, value)

    def pop(self, key):
        return self._map.pop(key, None)

    def export(self, filename):
        assert filename != ''
        with open(filename, 'w', encoding='utf8') as file:
            import json
            json.dump(self._map, file, indent=4, ensure_ascii=False)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Storage, cls).__new__(cls)
        return cls.instance

