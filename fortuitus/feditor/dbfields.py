from django.db import models
from south.modelsinspector import add_introspection_rules

class ParamsField(models.TextField):
    pass


add_introspection_rules([], ["^fortuitus\.feditor\.dbfields\.ParamsField"])