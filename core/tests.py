from django.test import TestCase
from django.contrib.auth.models import User


class BaseTestCase(TestCase):
    def assertObject(self, instance, **params):
        """
        Asserts that object have given attributes of given values.

        Sample usage:

            # Fetches user from DB and asserts that username=='bob'
            self.assertObject(user, username='bob')
        """
        for attr, expected in params.iteritems():
            attr_name, _, comparator = attr.partition('__')
            comparator = comparator or 'eq'
            value = getattr(instance, attr_name)
            if isinstance(value, property):
                value = get
            if comparator == 'eq':
                self.assertEqual(expected, value, 'Failed assertion on %s: %s should equal %s'% (attr_name, value, expected))
            elif comparator == 'gte':
                self.assertGreaterEqual(value, expected, 'Failed assertion on %s: %s should be greater or equal to %s' % (attr_name, value, expected))
            else:
                raise ValueError('Unknown comparator: %s' % comparator)

    def assertModel(self, model, pk, **params):
        """
        Fetches object (of given model) with pk=pk, then asserts that
        attributes updated.

        Sample usage:

            # Fetches user from DB and asserts that username=='bob'
            self.assertModel(User, 1, username='bob')

        """
        self.assertObject(model.objects.get(pk=pk), **params)

    def assertObjectUpdated(self, old_instance, **params):
        """
        Fetches object (of given model) with pk=pk, then asserts that
        attributes updated.

        Sample usage:

            # Fetches user_instance from DB again and asserts username=='john'
            self.assertObjectUpdated(user_instance, username='john')

        """
        self.assertModel(old_instance.__class__, old_instance.pk, **params)

    def login_user(self, username='username', password='password'):
        user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)
        return user
