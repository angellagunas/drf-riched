# -*- coding: utf-8 -*-


def autodiscover():
    """
    Perform an autodiscover of an viewsets.py file in the installed apps to
    generate the routes of the registered viewsets.
    """
    from polls import routes  # noqa
