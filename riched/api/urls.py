# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from . import v1


urlpatterns = [
    url(
        r'^v1/', include('api.v1.urls', namespace='v1')
    ),
]
#
# urlpatterns += [
#     url(
#         r'^docs/', include('rest_framework_swagger.urls')
#     ),
# ]
