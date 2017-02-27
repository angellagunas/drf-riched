# -*- coding: utf-8 -*-
from . import viewsets
from riched.api.v1.routers import router


router.register(
    r"polls",
    viewsets.PollViewSet,
    base_name="polls",
)

router.register(
    r"questions",
    viewsets.QuestionViewSet,
    base_name="questions",
)
