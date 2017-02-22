# -*- coding: utf-8 -*-
from some.management.core.api import mixins

from riched.api.v1.routers import router
from some.management.core.api.viewsets import GenericViewSet

from riched.polls import serializers
from riched.polls.models import (
    Question,
)


class QuestionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.PartialUpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    list_serializer_class = serializers.QuestionListSerializer
    retrieve_serializer_class = serializers.QuestionRetrieveSerializer
    create_serializer_class = serializers.QuestionCreateSerializer
    update_serializer_class = serializers.QuestionUpdateSerializer

    permission_classes = []  # put your custom permissions here

    def create(self, request, *args, **kwargs):
        """
        Allows create a Question in riched.
        ---
        request_serializer: serializers.QuestionCreateSerializer
        response_serializer: serializers.QuestionRetrieveSerializer
        responseMessages:
            - code: 201
                message: CREATED
            - code: 400
                message: BAD REQUEST
            - code: 403
                message: FORBIDDEN
            - code: 500
                message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        return super(QuestionViewSet, self).create(
            request, *args, **kwargs
        )

    def list(self, request, *args, **kwargs):
        """
        Returns a list of riched Question.
        ---
        response_serializer: serializers.QuestionListSerializer
        responseMessages:
            - code: 200
              message: OK
            - code: 404
              message: NOT FOUND
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        return super(QuestionViewSet, self).list(
            request, *args, **kwargs
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves information about a riched Question.
        ---
        response_serializer: serializers.QuestionRetrieveSerializer
        responseMessages:
            - code: 200
              message: OK
            - code: 403
              message: FORBIDDEN
            - code: 404
              message: NOT FOUND
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        return super(QuestionViewSet, self).retrieve(
            request, *args, **kwargs
        )

    def partial_update(self, request, pk=None):
        """
        Updates a Question.
        ---
        request_serializer: serializers.QuestionUpdateSerializer
        response_serializer: serializers.QuestionRetrieveSerializer
        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: BAD REQUEST
            - code: 403
              message: FORBIDDEN
            - code: 404
              message: NOT FOUND
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        return super(QuestionViewSet, self).partial_update(request)

    def destroy(self, request, pk=None):
        """
        Deletes a Question.
        ---
        responseMessages:
            - code: 204
              message: NO CONTENT
            - code: 400
              message: BAD REQUEST
            - code: 403
              message: FORBIDDEN
            - code: 404
              message: NOT FOUND
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        return super(QuestionViewSet, self).destroy(request)

    def get_queryset(self, *args, **kwargs):
        queryset = Question.objects.all()
        return queryset


router.register(
    r"questions",
    QuestionViewSet,
    base_name="questions",
)
