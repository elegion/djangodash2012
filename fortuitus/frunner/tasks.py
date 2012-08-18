from celery import task


@task()
def add(x, y):
    """ Test task. """
    return x + y
