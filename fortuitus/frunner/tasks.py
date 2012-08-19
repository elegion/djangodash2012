from celery import task
from django.forms.models import model_to_dict

from fortuitus.feditor import models as emodels
from fortuitus.frunner import models as rmodels


@task()
def add(x, y):
    """ Test task. """
    return x + y


@task()
def run_tests(project_id):
    """
    A task that actually runs the API testing.

    First it copies the test data to the run history tables, then runs the
    tests.

    """
    # Obtain project to run
    project = emodels.TestProject.objects.get(pk=project_id)

    testrun = rmodels.TestRun.objects.create(project=project,
                                             base_url=project.base_url,
                                             common_params=project.common_params)
    # Now copy all testcases and related data
    for etest in project.testcases.all():
        kwargs = model_to_dict(etest, exclude=['id', 'project'])
        rtest = rmodels.TestCase.objects.create(testrun=testrun, **kwargs)

        for estep in etest.steps.all():
            kwargs = model_to_dict(estep, exclude=['testcase'])
            rstep = rmodels.TestCaseStep.objects.create(testcase=rtest, **kwargs)

            for assertion in estep.assertions.all():
                kwargs = model_to_dict(assertion, exclude=['step'])
                rmodels.TestCaseAssert.objects.create(step=rstep, **kwargs)

    testrun.run()
