DRF_SETTINGS = {
    'exclude_apps': ['admin', 'contenttypes', 'auth', 'sessions'],
    'include_apps': [],
    'version': 1,
    'api': {
        'mixins': 'some.management.core.api.mixins',
        'routers': 'some.management.core.api.routers',
        'serializers': 'some.management.core.api.serializers',
        'viewsets': 'some.management.core.api.viewsets'
    }
}
