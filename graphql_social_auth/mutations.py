import graphene


from django.utils.translation import ugettext_lazy as _

from social_core.exceptions import MissingBackend
from .utils import load_backend, load_strategy
from social_django.views import _do_login
from social_core.utils import user_is_authenticated, \
                   user_is_active, partial_pipeline_data

from . import exceptions, results

               
class AbstractSocialAuthMutation(graphene.Mutation):

    class Meta:
        abstract = True

    class Arguments:
        provider = graphene.String(required=True)

    @classmethod
    def get_backend(cls, request, provider, **kwargs):
        strategy = load_strategy(request, **kwargs)

        try:
            backend = load_backend(strategy, provider, redirect_uri=None)
        except MissingBackend:
            raise exceptions.GraphQLSocialAuthError(_('Provider not found'))
        return backend

    @classmethod
    def mutate(cls, root, info, provider, **kwargs):
        backend = cls.get_backend(info.context, provider, **kwargs)
        return results.SocialAuthResult(result=backend.start())


class AbstractSocialAuthCompleteMutation(graphene.Mutation):

    class Meta:
        abstract = True

    class Arguments:
        providerData = graphene.JSONString(default_value={})
        provider = graphene.String(required=True)

    @classmethod
    def get_backend(cls, request, provider, **kwargs):
        strategy = load_strategy(request, **kwargs)

        try:
            backend = load_backend(strategy, provider, redirect_uri=None)
        except MissingBackend:
            raise exceptions.GraphQLSocialAuthError(_('Provider not found'))
        return backend

    @classmethod
    def do_login(cls, backend, user, social_user):
        pass

    @classmethod
    def get_result(cls,
            backend,
            user,
            is_successful_login,
            is_inactive_user,
            is_new,
            is_new_association,
            **kwargs):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def mutate(cls, root, info, provider, **kwargs):
        backend = cls.get_backend(info.context, provider, **kwargs)

        data = backend.strategy.request_data()
        
        user = info.context.user

        is_authenticated = user_is_authenticated(user)
        user = user if is_authenticated else None

        partial = partial_pipeline_data(backend, user)
        if partial:
            user = backend.continue_pipeline(partial)
            # clean partial data after usage
            backend.strategy.clean_partial_pipeline(partial.token)
        else:
            user = backend.complete(user=user)

        if user is None:
            raise exceptions.InvalidTokenError(_('Invalid token'))

        # check if the output value is something else than a user and just
        # return it to the client
        user_model = backend.strategy.storage.user.user_model()
        if isinstance(user, graphene.ObjectType):
            return user

        elif not isinstance(user, user_model):
            msg = _('`{}` is not a user or graphene.ObjectType instance').format(type(user).__name__)
            raise exceptions.DoAuthError(msg, user)

        is_inactive_user = False
        is_new_association = False
        is_successful_login = False

        if is_authenticated:
            if user:
                is_new_association = True

        elif user:
            if user_is_active(user):
                # catch is_new/social_user in case login() resets the instance
                is_new = getattr(user, 'is_new', False)
                social_user = user.social_user
                cls.do_login(backend, user, social_user)
                # store last login backend name in session
                backend.strategy.session_set('social_auth_last_login_backend',
                                             social_user.provider)
                is_successful_login = True
            else:
                if backend.setting('INACTIVE_USER_LOGIN', False):
                    social_user = user.social_user
                    cls.do_login(backend, user, social_user)
                    is_successful_login = True
                is_inactive_user = True

        return cls(result=cls.get_result(
            backend,
            user,
            is_successful_login,
            is_inactive_user,
            is_new,
            is_new_association,
            **kwargs))


class SocialAuth(AbstractSocialAuthMutation):
    """Social Auth Mutation"""

    result = graphene.Field(results.SocialAuthResult)


class SocialAuthComplete(AbstractSocialAuthCompleteMutation):
    """Social Auth Mutation"""

    result = graphene.Field(results.SocialAuthCompleteResult)

    @classmethod
    def do_login(cls, backend, user, social_user):
        _do_login(backend, user, social_user)

    @classmethod
    def get_result(cls,
            backend,
            user,
            is_successful_login,
            is_inactive_user,
            is_new,
            is_new_association,
            **kwargs):
        return results.Social(social=user.social_user,
            is_successful_login = is_successful_login,
            is_inactive_user = is_inactive_user,
            is_new = is_new,
            is_new_association = is_new_association)


class SocialAuthJWTComplete(AbstractSocialAuthCompleteMutation):
    """Social Auth for JSON Web Token (JWT)"""

    result = graphene.Field(results.SocialAuthJWTCompleteResult)

    @classmethod
    def get_result(cls,
            backend,
            user,
            is_successful_login,
            is_inactive_user,
            is_new,
            is_new_association,
            **kwargs):
        try:
            from graphql_jwt.shortcuts import get_token
        except ImportError:
            raise ImportError(
                'django-graphql-jwt not installed.\n'
                'Use `pip install \'django-graphql-social-auth[jwt]\'`.')
        return results.JWT(social=user.social_user,
            token=get_token(user),
            is_successful_login = is_successful_login,
            is_inactive_user = is_inactive_user,
            is_new = is_new,
            is_new_association = is_new_association)
