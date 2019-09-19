from django.conf import settings
from social_core.utils import setting_name, module_member, get_strategy
from social_core.exceptions import MissingBackend
from social_core.backends.utils import get_backend

BACKENDS = settings.AUTHENTICATION_BACKENDS
STRATEGY = getattr(settings, setting_name('STRATEGY'),
                   'graphql_social_auth.strategy.GraphqlStrategy')
STORAGE = getattr(settings, setting_name('STORAGE'),
                  'social_django.models.DjangoStorage')
Strategy = module_member(STRATEGY)
Storage = module_member(STORAGE)


def load_strategy(request=None):
    return get_strategy(STRATEGY, STORAGE, request)


def load_backend(strategy, name, redirect_uri):
    Backend = get_backend(BACKENDS, name)
    return Backend(strategy, redirect_uri)
