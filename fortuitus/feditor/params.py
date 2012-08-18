from __future__ import unicode_literals
import json
import random
import string
from django.utils.importlib import import_module

class Params(dict):
    def dumps(self):
        data = {}
        for name, value in self.items():
            data[name] = {
                'module': value.__class__.__module__,
                'class': value.__class__.__name__}
            data[name].update(value.as_dict())
        return json.dumps(data)

    @staticmethod
    def loads(s):
        data = json.loads(s)
        params = Params()
        for name, value in data.items():
            module = value.pop('module')
            klass = value.pop('class')
            params[name] = getattr(import_module(module), klass).from_dict(value)
        return params

    def __unicode__(self):
        return self.dumps()


class ParamValue(object):
    def __init__(self):
        pass

    def __unicode__(self):
        pass

    def as_dict(self):
        return dict((k,v) for k,v in self.__dict__.items() if not k.startswith('_'))

    @classmethod
    def from_dict(klass, params):
        return klass(**params)


class PlainValue(ParamValue):
    value = None

    def __init__(self, value):
        super(PlainValue, self).__init__()
        self.value = value

    def __unicode__(self):
        return self.value


class RandomValue(ParamValue):
    def __init__(self, length=6, symbols=string.ascii_lowercase):
        super(RandomValue, self).__init__()
        self.length = length
        self.symbols = symbols
        self.__value = None

    def generate(self):
        return ''.join([random.choice(self.symbols) for n in xrange(self.length)])

    def __unicode__(self):
        if self.__value is None:
            self.__value = self.generate()
        return self.__value

