import json
from django.db import models
from south.modelsinspector import add_introspection_rules


class ParamsField(models.TextField):
    __metaclass__ = models.SubfieldBase

    description = u'Store query params, like GET params: login=test, password=test'

    def to_python(self, value):
        if isinstance(value, dict):
            return value
        else:
            if not value:
                return value
            return json.loads(str(value))

    def get_prep_value(self, value):
        if value is not None and not isinstance(value, basestring):
            if isinstance(value, dict):
                value = json.dumps(value)
            else:
                raise TypeError('Not a dictionary.')
        return value

    def get_internal_type(self):
        return 'TextField'


add_introspection_rules([], ["^fortuitus\.feditor\.dbfields\.ParamsField"])