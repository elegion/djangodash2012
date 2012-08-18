import string

from django.test import TestCase

from fortuitus.fcore.models import Company
from fortuitus.feditor.dbfields import ParamsField
from fortuitus.feditor.models import TestProject
from fortuitus.feditor.params import Params, PlainValue, RandomValue


class ParamsTestCase(TestCase):
    def test_serialize(self):
        """ Tests params serialization. """
        length = 6
        symbols = string.digits
        login = 'test_login'

        params = Params()
        params['login'] = PlainValue('test_login')
        params['password'] = RandomValue(length=6, symbols=symbols)
        password = unicode(params['password'])

        params2 = Params().loads(params.dumps())
        self.assertEquals(unicode(params2['login']), login)
        password2 = unicode(params2['password'])
        self.assertEquals(len(password2), length)
        for char in password2:
            self.assertTrue(char in symbols)
        #random should regenerate each time
        self.assertNotEquals(password2, password)

    def test_plain(self):
        """ Tests PlainValue. """
        param = Params()
        param['login'] = PlainValue('test_login')
        param['password'] = PlainValue('test_password')
        self.assertEquals(unicode(param['login']), 'test_login')
        self.assertEquals(unicode(param['password']), 'test_password')

    def test_random(self):
        """ Tests RandomValue. """
        length = 5
        symbols = string.ascii_letters

        param = Params()
        param['login'] = RandomValue(length=length, symbols=symbols)

        login = unicode(param['login'])
        self.assertEquals(len(login), 5)
        self.assertTrue(all(c in symbols for c in login))

        new_login = unicode(param['login'])
        self.assertEquals(login, new_login)

        # Random should be different at least 10 times.
        for x in xrange(10):
            param['login'] = RandomValue(length=length, symbols=symbols)
            new_login = unicode(param['login'])
            self.assertNotEquals(login, new_login)


class ParamsFieldTestCase(TestCase):
    def test_inmodel(self):
        """ Tests params field. """
        login = 'test_login'
        length = 7
        symbols = string.ascii_letters

        company = Company.objects.create(name='test')
        proj = TestProject(name='test', company=company,
            base_url='http://example.com', common_params=Params())
        proj.common_params['login'] = PlainValue('test_login')
        proj.common_params['password'] = RandomValue(length, symbols)
        proj.save()

        pk = proj.pk

        proj2 = TestProject.objects.get(pk=pk)
        password = unicode(proj2.common_params['password'])
        self.assertEquals(login, unicode(proj2.common_params['login']))
        self.assertEquals(len(password), length)
        self.assertTrue(all(c in symbols for c in password))
