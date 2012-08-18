from django.utils.unittest import TestCase


class BaseTestCase(TestCase):
    def assertModel(self, model, id, **params):
        instance = model.objects.get(pk=id)
        for attr, expected in params.iteritems():
            attr_name, _, comparator = attr.partition('__')
            comparator = comparator or 'eq'
            value = getattr(instance, attr_name)
            if comparator == 'eq':
                self.assertEqual(expected, value)
            elif comparator == 'gte':
                self.assertGreaterEqual(value, expected)
            else:
                raise ValueError('Unknown comparator: %s' % comparator)

    def assertObjectUpdated(self, old_instance, **params):
        self.assertModel(old_instance.__class__, old_instance.pk, **params)
