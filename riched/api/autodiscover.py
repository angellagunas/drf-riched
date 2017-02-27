# -*- coding: utf-8 -*-
from importlib import import_module

from django.conf import settings


def autodiscover():
    """
    Perform an autodiscover of an viewsets.py file in the installed apps to
    generate the routes of the registered viewsets.
    """
    for app in settings.INSTALLED_APPS:
        try:
            import_module('.'.join((app, 'routes')))

        except ImportError, e:
            if e.message != 'No module named api' and settings.DEBUG:
                print e.message
            else:
                print e
                pass
