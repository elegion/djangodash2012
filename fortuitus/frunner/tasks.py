from celery import task
from django.forms.models import model_to_dict

from fortuitus.feditor import models as emodels
from fortuitus.frunner import models as rmodels


@task()
def add(x, y):
    """ Test task. """
    return x + y


@task()
def run_tests(test_id):
    """
    A task that actually runs the API testing.

    First it copies the test data to the run history tables, then runs the
    tests.

    """
    # Obtain testcase to run
    etest = emodels.TestCase.objects.get(pk=test_id)

    # Now copy test and all related data
    kwargs = model_to_dict(etest, exclude=['id', 'project'])
    rtest = rmodels.TestCase.objects.create(project=etest.project, **kwargs)

    for estep in etest.steps.all():
        kwargs = model_to_dict(estep, exclude=['testcase'])
        rstep = rmodels.TestCaseStep.objects.create(testcase=rtest, **kwargs)

        for assertion in estep.assertions.all():
            kwargs = model_to_dict(assertion, exclude=['step'])
            rmodels.TestCaseAssert.objects.create(step=rstep, **kwargs)

    rtest.run()
