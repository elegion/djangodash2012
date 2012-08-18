from __future__ import unicode_literals
import json
import random
import string

from core.cache import cached_property
from django.utils.importlib import import_module


class Params(dict):
    """ Represents query parameters, JSON serializable. """
    def dumps(self):
        """ Serialize parameters in JSON format. """
        data = {}
        for name, value in self.items():
            data[name] = {
                'module': value.__class__.__module__,
                'class': value.__class__.__name__}
            data[name].update(value.as_dict())
        return json.dumps(data)

    @staticmethod
    def loads(s):
        """ Load parameters from JSON format. """
        data = json.loads(s)
        params = Params()
        for name, value in data.items():
            module = value.pop('module')
            klass = value.pop('class')
            params[name] = getattr(import_module(module),
                                   klass).from_dict(value)
        return params

    def __unicode__(self):
        return self.dumps()


class ParamValue(object):
    """ Query parameter value base class. """
    def as_dict(self):
        """ Convert value to dictionary. """
        return dict((k, v) for k, v in self.__dict__.items()
                    if not k.startswith('_'))

    @classmethod
    def from_dict(klass, params):
        """ Create value from dictionary. """
        return klass(**params)


class PlainValue(ParamValue):
    """
    Plain value, like string.

    :param value: the value itself.

    """
    value = None

    def __init__(self, value):
        super(PlainValue, self).__init__()
        self.value = value

    def __unicode__(self):
        return self.value


class RandomValue(ParamValue):
    """
    Randomly generated string based on alphabet.

    :param length: generated string length.
    :param symbols: list of symbols to be used in string generation.

    """
    def __init__(self, length=6, symbols=string.ascii_lowercase):
        super(RandomValue, self).__init__()
        self.length = length
        self.symbols = symbols

    @cached_property
    def _value(self):
        return self.generate()

    def generate(self):
        return ''.join(random.choice(self.symbols)
                       for n in xrange(self.length))

    def __unicode__(self):
        return self._value
