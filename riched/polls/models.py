# -*- coding_ utf-8 -*-

from django.db import models


class Poll(models.Model):
    class Meta:
        drf_config = {
            'api': {
                'scaffolding': True,
                'methods': ['CREATE', 'UPDATE'],
                'serializer': {
                    'scaffolding': True,
                    'fields': [
                        'title'
                    ]
                }
            }
        }

    title = models.CharField(max_length=100)
    body = models.CharField(max_length=100)


class Question(models.Model):
    class Meta:
        drf_config = {
            'api': {
                'scaffolding': True,
                'serializer': {
                    'scaffolding': True
                }
            }
        }
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=100)
