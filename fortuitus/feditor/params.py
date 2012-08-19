from __future__ import unicode_literals
import json
import re

from fortuitus.feditor.resolvers import resolve_param
from django.utils.datastructures import SortedDict


class Params(SortedDict):
    """ Represents query parameters, JSON serializable."""
    def __init__(self, **params):
        """Emulate dict init"""
        super(Params, self).__init__(data=params)

    def dumps(self):
        """ Serialize parameters in JSON format. """
        return json.dumps(self)

    @staticmethod
    def loads(s):
        """ Load parameters from JSON format. """
        data = json.loads(s)
        params = Params()
        for name in sorted(data):
            params[name] = data[name]
        return params

    def resolve(self, context={}):
        """ Resolves all params values
        """
        result = Params()
        for name, value in self.iteritems():
            result[name] = resolve_param(value, context)
        return result

    def __unicode__(self):
        return self.dumps()