from celery import task


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
    # TODO
    pass
