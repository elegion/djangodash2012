from django.core.urlresolvers import reverse
from django.test import TestCase


class HomeViewTestCase(TestCase):
    def test_renders_template(self):
        """ Tests is home page is rendered properly. """
        response = self.client.get(reverse('home'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('fortuitus/fcore/home.html')
