import logging
from django.conf import settings


class RequireDebugTrue(logging.Filter):
    def filter(self, record):
        return settings.DEBUG
