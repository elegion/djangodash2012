from __future__ import unicode_literals
import json
import re


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

    def __unicode__(self):
        return self.dumps()