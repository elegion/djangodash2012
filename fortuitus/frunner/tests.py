from django.test import TestCase


class TaskTestCase(TestCase):
    def test_add(self):
        """
        Tests that 1 + 1 always equals 2. Asynchronously!
        """
        from fortuitus.frunner.tasks import add
        result = add.delay(1, 1)
        self.assertEqual(result.result, 2)
