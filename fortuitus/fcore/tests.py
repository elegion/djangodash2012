from django.core.urlresolvers import reverse
from django.test import TestCase

from core.tests import BaseTestCase
from fortuitus.fcore.factories import UserF, CompanyF
from fortuitus.fcore.models import FortuitusProfile


class HomeViewTestCase(TestCase):
    def test_renders_template(self):
        """ Tests if home page is rendered properly. """
        response = self.client.get(reverse('home'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('fortuitus/fcore/home.html')


class ProfileTestCase(TestCase):
    def test_profile_created(self):
        """ Tests that profile is automatically created along with User. """
        u = UserF.create()
        p = FortuitusProfile.objects.all()[0]
        self.assertEqual(u.fortuitusprofile, p)

    def test_profiles_not_conflicted(self):
        """
        Tests that second profile is created and not conflicted with the first
        user nor his profile.
        """
        u1 = UserF.create(username='u1')
        p1 = FortuitusProfile.objects.get(user_id=u1.pk)
        u2 = UserF.create(username='u2')
        p2 = FortuitusProfile.objects.get(user_id=u2.pk)
        self.assertNotEqual(p1, p2)


class ProjectsListTestCase(BaseTestCase):
    def test_renders_template(self):
        """ Tests if projects list page is rendered properly. """
        user = self.login_user()
        company = CompanyF.create()
        user.fortuitusprofile.company = company
        user.fortuitusprofile.save()
        url = reverse('fcore_projects_list',
                      kwargs={'company_slug': company.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('fortuitus/fcore/projects_list.html')

    def test_requires_login(self):
        """ Tests if projects list page is rendered properly. """
        company = CompanyF.create()
        url = reverse('fcore_projects_list',
                      kwargs={'company_slug': company.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class QueryCountTestCase(BaseTestCase):
    def test_home_page(self):
        with self.assertNumQueries(0):
            self.client.get(reverse('home'))

    def test_sign_up(self):
        with self.assertNumQueries(0):
            self.client.get(reverse('signup'))

    def test_demo(self):
        with self.assertNumQueries(18):
            self.client.get(reverse('demo'))

    def test_project_list(self):
        self.client.get(reverse('demo'))
        with self.assertNumQueries(6):
            self.client.get(reverse('fcore_projects_list',
                                    kwargs={'company_slug': 'demo'}))
