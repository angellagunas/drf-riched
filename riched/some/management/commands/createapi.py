# -*- coding: utf-8 -*-
import os
import sys

from django.apps import apps
from django.core.management import BaseCommand
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template import Template, Context

from . import templates


class Command(BaseCommand):
    help = "Starts an api from app models for development."

    can_import_settings = True
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='app_label', nargs='*',
            help='Name of the application where you want create the api.',
        )

    def write(self, msg):
        self.stderr.write(msg)

    def handle(self, *app_labels, **options):
        exclude_apps = ['admin', 'contenttypes', 'auth', 'sessions']

        if len(app_labels) == 0:
            app_labels = ContentType.objects.exclude(
                app_label__in=exclude_apps
            ).values_list(
                'app_label',
                flat=True
            ).distinct()

        # Make sure the app they asked for exists
        app_labels = set(app_labels)
        bad_app_labels = set()
        given_apps_path = []
        PROJECT_NAME = settings.BASE_DIR.split('/')[-1]

        for app_label in app_labels:
            try:
                app = apps.get_app_config(app_label)
                models = []
                for m in apps.get_app_config(app_label).get_models():
                    if hasattr(m._meta, 'api_drf'):
                        if m._meta.api_drf is True:
                            models.append(m)

                given_apps_path.append({
                    'path': app.path,
                    'label': app_label,
                    'api_path': "{0}/api.py".format(app.path),
                    'serializer_path': "{0}/serializer.py".format(app.path),
                    'models': [m.__name__ for m in models],
                    'extra_options': {}
                })
            except LookupError:
                bad_app_labels.add(app_label)

        if bad_app_labels:
            for app_label in bad_app_labels:
                msg = "App '%s' could not be found." % app_label
                self.write(msg)
            sys.exit(2)

        #
        # Validate applications path exists
        #
        if given_apps_path:
            for app in given_apps_path:
                if not os.path.isfile(app['api_path']):
                    msg = 'serializer is already exist in app: %s' % app['label']  # noqa
                    self.write(msg)

                if not os.path.isfile(app['serializer_path']):
                    msg = 'api is already exist in app: %s' % app['label']
                    self.write(msg)
            sys.exit(2)

        else:
            self.write("Apps could not be found.")
            sys.exit(2)

        for app in given_apps_path:
            #
            # Crate serializer file
            #
            with open(app["serializer_path"], "w") as f:
                context = Context({
                    'project_name': PROJECT_NAME,
                    'app_name': app['label'],
                    'model_list': app['models']
                })

                template = Template(templates.SERIALIZER_TEMPLATE)
                api_text = template.render(context)
                f.write(api_text)

            #
            # Create api file
            #
            with open(app["api_path"], "w") as f:
                context = Context({
                    'project_name': PROJECT_NAME,
                    'app_name': app['label'],
                    'api_version': '1',
                    'model_list': app['models']
                })

                template = Template(templates.API_TEMPLATE)
                api_text = template.render(context)
                f.write(api_text)
