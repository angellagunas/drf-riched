# -*- coding: utf-8 -*-
API_TEMPLATE = '''# -*- coding: utf-8 -*-
from some.management.core.api import mixins
from some.management.core.api.viewsets import GenericViewSet

from {{project_name}}.{{app_name}} import serializers
from {{project_name}}.{{app_name}}.models import {{model.name}}


class {{model.name}}ViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.PartialUpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    list_serializer_class = serializers.{{model.name}}ListSerializer
    retrieve_serializer_class = serializers.{{model.name}}RetrieveSerializer
    create_serializer_class = serializers.{{model.name}}CreateSerializer
    update_serializer_class = serializers.{{model.name}}UpdateSerializer

    permission_classes = []  # put your custom permissions here

    def create(self, request, *args, **kwargs):
        """
        Allows create a {{model.name}} in {{project_name}}.
        ---
        request_serializer: serializers.{{model.name}}CreateSerializer
        response_serializer: serializers.{{model.name}}RetrieveSerializer
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
        return super({{model.name}}ViewSet, self).create(
            request, *args, **kwargs
        )

    def list(self, request, *args, **kwargs):
        """
        Returns a list of {{project_name}} {{model.name}}.
        ---
        response_serializer: serializers.{{model.name}}ListSerializer
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
        return super({{model.name}}ViewSet, self).list(
            request, *args, **kwargs
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves information about a {{project_name}} {{model.name}}.
        ---
        response_serializer: serializers.{{model.name}}RetrieveSerializer
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
        return super({{model.name}}ViewSet, self).retrieve(
            request, *args, **kwargs
        )

    def partial_update(self, request, pk=None):
        """
        Updates a {{model.name}}.
        ---
        request_serializer: serializers.{{model.name}}UpdateSerializer
        response_serializer: serializers.{{model.name}}RetrieveSerializer
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
        return super({{model.name}}ViewSet, self).partial_update(request)

    def destroy(self, request, pk=None):
        """
        Deletes a {{model.name}}.
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
        return super({{model.name}}ViewSet, self).destroy(request)

    def get_queryset(self, *args, **kwargs):
        queryset = {{model.name}}.objects.all()
        return queryset
'''

ROUTE_TEMPLATE = '''# -*- coding: utf-8 -*-
from . import viewsets
from {{project_name}}.api.v{{api_version}}.routers import router


{% for model in models %}router.register(
    r"{{model.name|lower}}s",
    viewsets.{{model.name}}ViewSet,
    base_name="{{model.name|lower}}s",
){% if not forloop.last %}\n\n{%endif%}{% endfor %}
'''

SERIALIZER_TEMPLATE = '''# -*- coding: utf-8 -*-
from some.management.core.api.serializers import ModelSerializer

from {{project_name}}.{{app_name}}.models import {{model.name}}


class {{model.name}}Serializer(ModelSerializer):

    class Meta:
        model = {{model.name}}
        fields = ({%if model.fields%}{%for field in model.fields%}
            '{{field}}',{%endfor%}{%else%}
            '__all__'{%endif%}
        )
'''

ROUTER_TEMPLATE = '''# -*- coding: utf-8 -*-
from some.management.core.api.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
'''

API_V1_URLS_TEMPLATE = '''# -*- coding: utf-8 -*-
from .routers import router
from ..autodiscover import autodiscover


autodiscover()

urlpatterns = router.urls
'''

API_URLS_TEMPLATE = '''# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url


urlpatterns = [
    url(
        r'^v1/', include('api.v1.urls', namespace='v1')
    ),
]

urlpatterns += [
    url(
        r'^docs/', include('rest_framework_swagger.urls')
    ),
]
'''

AUTODISCOVER_TEMPLATE = '''# -*- coding: utf-8 -*-
from importlib import import_module


def autodiscover():
    """
    Perform an autodiscover of an viewsets.py file in the installed apps to
    generate the routes of the registered viewsets.
    """
    for app in settings.INSTALLED_APPS:
        try:
            import_module('.'.join((app, 'viewsets')))

        except ImportError, e:
            if e.message != 'No module named api' and settings.DEBUG:
                print e.message
            else:
                pass
'''
