# -*- coding: utf-8 -*-
from .viewsets import (
    question,
)
from api.v1.routers import router


router.register(
    r"questions",
    question.QuestionViewSet,
    base_name="questions",
)
