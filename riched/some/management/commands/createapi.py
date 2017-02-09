# -*- coding: utf-8 -*-
import os
import sys

from django.apps import apps
from django.core.management import BaseCommand
from django.conf import settings
from django.template import Template, Context

from . import api_template


class Command(BaseCommand):
    help = "Starts an api from app models for development."

    can_import_settings = True
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='app_label', nargs='*',
            help='Name of the application where you want create the api.',
        )

    def handle(self, *app_labels, **options):

        # Make sure the app they asked for exists
        app_labels = set(app_labels)
        bad_app_labels = set()
        given_apps_path = []
        PROJECT_NAME = settings.BASE_DIR.split('/')[-1]

        for app_label in app_labels:
            try:
                app = apps.get_app_config(app_label)
                given_apps_path.append({
                    'path': app.path,
                    'label': app_label,
                    'api_path': "{0}/api.py".format(app.path)
                })
            except LookupError:
                bad_app_labels.add(app_label)

        if bad_app_labels:
            for app_label in bad_app_labels:
                self.stderr.write(
                        "App '%s' could not be found. "
                        "Is it in INSTALLED_APPS?" % app_label
                )
            sys.exit(2)

        if given_apps_path:
            for app in given_apps_path:
                if not os.path.isfile("{}/api.py".format(app['path'])):
                    self.stdout.write(
                        'Writing api to app: {0}'.format(app['label'])
                    )
                    with open(app["api_path"], "w") as f:
                        context = Context({
                            'project_name': PROJECT_NAME,
                            'app_name': app['label'],
                            'model_list': ['Poll']
                        })

                        template = Template(api_template.API_TEMPLATE)
                        api_text = template.render(context)
                        f.write(api_text)
                else:
                    self.stdout.write(
                        'api is already exist in app: {}'.format(app['label'])
                    )

    def write_api(self, **options):
        print 'run run run :), creating api, u are cool!'
