# -*- coding: utf-8 -*-
import os
import sys

from django.apps import apps
from django.core.management import BaseCommand
from django.conf import settings as dj_settings
from django.contrib.contenttypes.models import ContentType
from django.template import Template, Context

from . import settings, templates


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

    def get_app_labels(self, app_labels):
        exclude_apps = settings.DRF_SETTINGS['exclude_apps']

        if len(app_labels) == 0:
            apps = ContentType.objects.exclude(
                app_label__in=exclude_apps
            ).values_list(
                'app_label',
                flat=True
            ).distinct()

            return set(apps)

        return set(app_labels)

    def write_file(self, f, context, template):
        template_loaded = Template(template)
        api_text = template_loaded.render(context)
        f.write(api_text)

    def write_serializer(self, config_app, model, project_name):
        #
        # Crate serializer file
        #
        serializer_path = '{0}{1}.py'.format(
            config_app['serializer_path'],
            model['name'].lower()
        )
        with open(serializer_path, "w") as f:
            context = Context({
                'project_name': project_name,
                'app_name': config_app['label'],
                'model': model
            })
            self.write_file(f, context, templates.SERIALIZER_TEMPLATE)
            f.close()

    def write_api(self, config_app, model, project_name):
        #
        # Create api file
        #
        viewset_path = '{0}{1}.py'.format(
            config_app['api_path'],
            model['name'].lower()
        )
        with open(viewset_path, "w") as f:
            context = Context({
                'project_name': project_name,
                'app_name': config_app['label'],
                'api_version': config_app['api_version'],
                'model': model
            })
            self.write_file(f, context, templates.API_TEMPLATE)
            f.close()

    def get_meta_model_config(self, model):
        if hasattr(model._meta, 'drf_config'):
            if model._meta.drf_config['api'] is True:
                model_config = {
                    'name': model.__name__,
                }

                if 'fields' in model._meta.drf_config:
                    model_config['fields'] = model._meta.drf_config['fields']

            return model_config

        return None

    def get_label_app_config(self, app_labels, api_version):
        given_apps_path = []
        bad_app_labels = set()
        for app_label in app_labels:
            try:
                app = apps.get_app_config(app_label)
                models = []
                for m in apps.get_app_config(app_label).get_models():
                    valid_model = self.get_meta_model_config(m)
                    if valid_model:
                        models.append(valid_model)

                given_apps_path.append({
                    'path': app.path,
                    'label': app_label,
                    'api_path': "{0}/viewsets/".format(app.path),
                    'serializer_path': "{0}/serializers/".format(app.path),
                    'models': models,
                    'api_version': api_version,
                    'extra_options': {}
                })
            except LookupError:
                bad_app_labels.add(app_label)

        if bad_app_labels:
            for app_label in bad_app_labels:
                msg = "App '%s' could not be found." % app_label
                self.write(msg)
            sys.exit(2)

        if not given_apps_path:
            self.write("Apps could not be found.")
            sys.exit(2)

        return given_apps_path

    def create_apps_dirs(self, app_path):
        if not os.path.exists(app_path):
            os.mkdir(app_path)

    def validate_paths(self, apps_path):
        for app in apps_path:
            api_path = '{0}'.format(app['api_path'])
            serializer_path = '{0}'.format(app['serializer_path'])
            for model in app['models']:
                api_file = '{0}{1}.py'.format(
                    api_path,
                    model['name'].lower()
                )
                serializer_file = '{0}{1}.py'.format(
                    serializer_path,
                    model['name'].lower()
                )
                if os.path.isfile(api_file):
                    msg = 'serializer is already exist in app: %s' % app['label']  # noqa
                    self.write(msg)

                if os.path.isfile(serializer_file):
                    msg = 'api is already exist in app: %s' % app['label']
                    self.write(msg)

    def handle(self, *app_labels, **options):
        PROJECT_NAME = dj_settings.BASE_DIR.split('/')[-1]
        API_VERSION = settings.DRF_SETTINGS['version']
        app_labels = self.get_app_labels(app_labels)

        #
        # Make sure the app they asked for exists
        #
        given_apps_path = self.get_label_app_config(app_labels, API_VERSION)

        #
        # Validate applications api path or serializer path exists
        #
        self.validate_paths(given_apps_path)

        for app in given_apps_path:
            self.create_apps_dirs(app['api_path'])
            self.create_apps_dirs(app['serializer_path'])
            for model in app['models']:
                self.write_api(app, model, PROJECT_NAME)
                self.write_serializer(app, model, PROJECT_NAME)
