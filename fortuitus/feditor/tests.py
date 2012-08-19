import string

from django.test import TestCase

from fortuitus.fcore.models import Company
from fortuitus.feditor.dbfields import ParamsField
from fortuitus.feditor.models import TestProject
from fortuitus.feditor.params import Params
from fortuitus.feditor.resolvers import resolve_param


class ParamsTestCase(TestCase):
    def test_serialize(self):
        """ Tests params serialization. """
        length = 6
        symbols = string.digits
        login = 'test_login'
        password = '{random:7:L}'

        params = Params()
        params['login'] = login
        params['password'] = password

        params2 = Params().loads(params.dumps())
        self.assertEquals(unicode(params2['login']), login)
        self.assertEquals(unicode(params2['password']), password)

    def test_resolve(self):
        """ Should return new Params() with all variables resolved
        """
        params = Params(login='Alex',
                        password='{random:32:dlL}')
        params2 = params.resolve()
        self.assertEqual('Alex', params2['login'])
        self.assertEqual(32, len(params2['password']))


class ParamsFieldTestCase(TestCase):
    def test_inmodel(self):
        """ Tests params field. """
        login = 'test_login'
        length = 7
        symbols = string.ascii_letters

        company = Company.objects.create(name='test')
        proj = TestProject(name='test', company=company,
            base_url='http://example.com', common_params=Params())
        proj.common_params['login'] = login
        proj.common_params['password'] = '{random:7:L}'
        proj.save()

        proj2 = TestProject.objects.get(pk=proj.pk)
        password = unicode(proj2.common_params['password'])
        self.assertEquals(login, unicode(proj2.common_params['login']))
        self.assertEquals(password, unicode(proj2.common_params['password']))


class ResolversTestCase(TestCase):
    def test_random_simple(self):
        login = ''
        #each time should be different
        for x in xrange(10):
            login2 = resolve_param('{random}', {})
            self.assertIsNotNone(login2)
            self.assertNotEquals(login, login2)
            login = login2

    def test_random_some(self):
        login = ''
        expr = '{random:11} test {random:13:d} test {random:15:dl_}@touchin.ru'
        #each time should be different
        for x in xrange(10):
            login2 = resolve_param(expr, {})
            self.assertEqual(len(expr), len(login2))
            self.assertIsNotNone(login2)
            self.assertNotEquals(login, login2)
            login = login2
