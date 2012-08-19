from django.core.urlresolvers import reverse
from django.test import TestCase

from fortuitus.fcore.factories import UserF
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
