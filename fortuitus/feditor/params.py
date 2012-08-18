from __future__ import unicode_literals
import random
import string


class Params(dict):
    pass


class ParamValue(object):
    def __init__(self):
        pass

    def __unicode__(self):
        pass


class PlainValue(ParamValue):
    value = None

    def __init__(self, value):
        super(PlainValue, self).__init__()
        self.value = value

    def __unicode__(self):
        return self.value

    def __iter__(self):
        return


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

