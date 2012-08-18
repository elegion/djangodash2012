import string
from django.test import TestCase
from fortuitus.feditor.dbfields import ParamsField
from fortuitus.feditor.params import Params, PlainValue, RandomValue

class ParamsTestCase(TestCase):
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

        #random should be different at least 10 times
        for x in xrange(10):
            param['login'] = RandomValue(length=length, symbols=symbols)
            new_login = unicode(param['login'])
            self.assertNotEquals(login, new_login)