import json
from django.db import models
from fortuitus.feditor.params import Params
from south.modelsinspector import add_introspection_rules


class ParamsField(models.TextField):
    __metaclass__ = models.SubfieldBase

    description = u'Store query Params, like GET params: login=test, password=test'

    def to_python(self, value):
        if isinstance(value, Params):
            return value
        else:
            if not value:
                return value
            return Params.loads(value)

    def get_prep_value(self, value):
        if value is not None and not isinstance(value, basestring):
            if isinstance(value, Params):
                value = value.dumps()
            else:
                raise TypeError('Not a Params class.')
        return value

    def get_internal_type(self):
        return 'TextField'


add_introspection_rules([], ["^fortuitus\.feditor\.dbfields\.ParamsField"])