class cached_property(object):
    """
    Property which caches the result of the given `getter`.

    """
    def __init__(self, getter):
        self.getter = getter
        for a in ['__module__', '__name__', '__doc__']:
            setattr(self, a, getattr(getter, a))

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__[self.__name__] = self.getter(obj)
        return value
