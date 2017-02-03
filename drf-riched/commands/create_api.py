# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Starts an api from app models for development."

    can_import_settings = True
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            'name',
            help='Name of the application where you want create the api.'
        )

    def handle(self, *args, **options):
        # from django.conf import settings
        """aqui va toda la logica del porgrama"""
        self.run(**options)

    def run(self, **options):
        """
        Runs the server, using the autoreloader if needed
        """
        print 'run run run server :)'
