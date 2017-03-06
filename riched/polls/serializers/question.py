# -*- coding: utf-8 -*-
from some.management.core.api.serializers import ModelSerializer

from polls.models import Question


class QuestionSerializer(ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'title',
        )
