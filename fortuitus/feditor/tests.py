import string

from django.test import TestCase

from fortuitus.feditor.dbfields import ParamsField
from fortuitus.feditor.params import Params, PlainValue, RandomValue


class ParamsTestCase(TestCase):
    def test_serialize(self):
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
        param = Params()
        param['login'] = PlainValue('test_login')
        param['password'] = PlainValue('test_password')
        self.assertEquals(unicode(param['login']), 'test_login')
        self.assertEquals(unicode(param['password']), 'test_password')

    def test_random(self):
        length = 5
        symbols = string.ascii_letters

        param = Params()
        param['login'] = RandomValue(length=length, symbols=symbols)

        login = unicode(param['login'])
        self.assertEquals(len(login), 5)
        for char in login:
            self.assertTrue(char in symbols)

        new_login = unicode(param['login'])
        self.assertEquals(login, new_login)

        # Random should be different at least 10 times.
        for x in xrange(10):
            param['login'] = RandomValue(length=length, symbols=symbols)
            new_login = unicode(param['login'])
            self.assertNotEquals(login, new_login)
