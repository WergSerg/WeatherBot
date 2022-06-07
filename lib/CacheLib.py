class ListDictBasedCache(object):
    __slots__ = ['__key2value', '__maxCount', '__weights']

    def __init__(self, maxCount=1000):
        self.__maxCount = maxCount
        self.__key2value = {}
        self.__weights = []

    def __updateWeight(self, key):
        try:
            self.__weights.remove(key)
        except ValueError:
            pass
        self.__weights.append(key)
        if len(self.__weights) > self.__maxCount:
            _key = self.__weights.pop(0)
            self.__key2value.pop(_key)

    def keys(self):
        return [x for x in self.__key2value]

    def __getitem__(self, key):
        try:
            value = self.__key2value[key]
            self.__updateWeight(key)
            return value
        except KeyError:
            self.__updateWeight(key)
            raise KeyError("key %s not found" % key)

    def __setitem__(self, key, value):
        self.__key2value[key] = value
        self.__updateWeight(key)

    def __str__(self):
        return str(self.__key2value)
