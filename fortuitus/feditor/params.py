from __future__ import unicode_literals
import json
import re

from fortuitus.feditor.resolvers import resolve_param


class Params(dict):
    """ Represents query parameters, JSON serializable."""
    def dumps(self):
        """ Serialize parameters in JSON format. """
        return json.dumps(self)

    @staticmethod
    def loads(s):
        """ Load parameters from JSON format. """
        data = json.loads(s)
        params = Params()
        for name, value in data.items():
            params[name] = value
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