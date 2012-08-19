from celery import task
from django.forms.models import model_to_dict

from fortuitus.feditor import models as emodels
from fortuitus.frunner import models as rmodels


@task()
def add(x, y):
    """ Test task. """
    return x + y


@task()
def run_tests(testrun_id):
    """
    A task that actually runs the API testing.

    Receives testrun_id, fetches it from database and all tests related to it
    (TestRun must be created earlier from TestProject, by calling TestRun.create_from(project))

    """
    testrun = rmodels.TestRun.objects.get(pk=testrun_id)
    testrun.run()
