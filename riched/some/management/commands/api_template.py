# -*- coding: utf-8 -*-
API_TEMPLATE = '''
# -*- coding: utf-8 -*-
from some.core.api import mixins

from {{project_name}}.api.v1.routers import router
from {{project_name}}.core.api.viewsets import GenericViewSet

from {{project_name}}.{{app_name}} import serializers
from {{project_name}}.{{app_name}}.models import (
    {% for model_name in model_list %}
    {{model_name}},
    {% endfor %}
)

{% for model_name in model_list %}
class {{model_name}}ViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.PartialUpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    list_serializer_class = serializers.{{model_name}}ListSerializer
    retrieve_serializer_class = serializers.{{model_name}}RetrieveSerializer
    create_serializer_class = serializers.{{model_name}}CreateSerializer
    update_serializer_class = serializers.{{model_name}}UpdateSerializer

    permission_classes = []  # put your custom permissions here

    def create(self, request, *args, **kwargs):
        """
        Allows create a {{model_name}} in {{project_name}}.
        ---
        request_serializer: serializers.{{model_name}}CreateSerializer
        response_serializer: serializers.{{model_name}}RetrieveSerializer
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
        return super({{model_name}}ViewSet, self).create(
            request, *args, **kwargs
        )

    def list(self, request, *args, **kwargs):
        """
        Returns a list of {{project_name}} {{model_name}}.
        ---
        response_serializer: serializers.{{model_name}}ListSerializer
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
        return super({{model_name}}ViewSet, self).list(
            request, *args, **kwargs
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves information about a {{project_name}} {{model_name}}.
        ---
        response_serializer: serializers.{{model_name}}RetrieveSerializer
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
        return super({{model_name}}ViewSet, self).retrieve(
            request, *args, **kwargs
        )

    def partial_update(self, request, pk=None):
        """
        Updates a {{model_name}}.
        ---
        request_serializer: serializers.{{model_name}}UpdateSerializer
        response_serializer: serializers.{{model_name}}RetrieveSerializer
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
        return super({{model_name}}ViewSet, self).partial_update(request)

    def destroy(self, request, pk=None):
        """
        Deletes a {{model_name}}.
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
        return super({{model_name}}ViewSet, self).destroy(request)

    def get_queryset(self, *args, **kwargs):
        queryset = {{model_name}}.objects.all()
        return queryset
{% endfor %}


{% for model_name in model_list %}
router.register(
    r"{{model_name|lower}}s",
    {{model_name}}ViewSet,
    base_name="{{model_name|lower}}s",
)
{% endfor %}
'''
