# -*- coding: utf-8 -*-
from some.management.core.api import mixins

from riched.api.v1.routers import router
from some.management.core.api.viewsets import GenericViewSet

from riched.polls import serializers
from riched.polls.models import Poll


class PollViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.PartialUpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    list_serializer_class = serializers.PollListSerializer
    retrieve_serializer_class = serializers.PollRetrieveSerializer
    create_serializer_class = serializers.PollCreateSerializer
    update_serializer_class = serializers.PollUpdateSerializer

    permission_classes = []  # put your custom permissions here

    def create(self, request, *args, **kwargs):
        """
        Allows create a Poll in riched.
        ---
        request_serializer: serializers.PollCreateSerializer
        response_serializer: serializers.PollRetrieveSerializer
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
        return super(PollViewSet, self).create(
            request, *args, **kwargs
        )

    def list(self, request, *args, **kwargs):
        """
        Returns a list of riched Poll.
        ---
        response_serializer: serializers.PollListSerializer
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
        return super(PollViewSet, self).list(
            request, *args, **kwargs
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves information about a riched Poll.
        ---
        response_serializer: serializers.PollRetrieveSerializer
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
        return super(PollViewSet, self).retrieve(
            request, *args, **kwargs
        )

    def partial_update(self, request, pk=None):
        """
        Updates a Poll.
        ---
        request_serializer: serializers.PollUpdateSerializer
        response_serializer: serializers.PollRetrieveSerializer
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
        return super(PollViewSet, self).partial_update(request)

    def destroy(self, request, pk=None):
        """
        Deletes a Poll.
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
        return super(PollViewSet, self).destroy(request)

    def get_queryset(self, *args, **kwargs):
        queryset = Poll.objects.all()
        return queryset


router.register(
    r"polls",
    PollViewSet,
    base_name="polls",
)
