# -*- coding: utf-8 -*-
from some.management.core.api.serializers import ModelSerializer

from riched.polls.models import Poll


class PollSerializer(ModelSerializer):

    class Meta:
        model = Poll
        fields = (
            '__all__'
        )
