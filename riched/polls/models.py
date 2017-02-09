# -*- coding_ utf-8 -*-

from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=100)


class Question(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=100)
