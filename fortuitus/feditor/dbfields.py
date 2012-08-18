from __future__ import unicode_literals

from django.db import models
from south.modelsinspector import add_introspection_rules

from fortuitus.feditor.params import Params


class ParamsField(models.TextField):
    """
    Serialized query parameters to store them in the database.

    """
    __metaclass__ = models.SubfieldBase

    description = 'Stores query params. E.g. GET params: login=test&password=test'

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
