from celery import task

from fortuitus.frunner import models as rmodels


@task()
def run_tests(testrun_id):
    """
    A task that actually runs the API testing.

    Receives testrun_id, fetches it from database and all tests related to it
    (TestRun must be created earlier from TestProject, by calling TestRun.create_from(project))

    """
    testrun = rmodels.TestRun.objects.get(pk=testrun_id)
    return testrun.run()
