import graphene


from django.utils.translation import ugettext_lazy as _

from social_core.exceptions import MissingBackend
from .utils import load_backend, load_strategy
from social_django.views import _do_login
from social_core.utils import user_is_authenticated, \
                   user_is_active, partial_pipeline_data

from . import exceptions, results

def get_backend(request, provider, **kwargs):
    strategy = load_strategy(request, **kwargs)

    try:
        backend = load_backend(strategy, provider, redirect_uri=kwargs.get('redirectUri'))
    except MissingBackend:
        raise exceptions.GraphQLSocialAuthError(_('Provider not found'))
    return backend
               
class AbstractSocialAuthMutation(graphene.Mutation):

    class Meta:
        abstract = True

    class Arguments:
        redirectUri = graphene.String(default_value=None) 
        provider = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, provider, **kwargs):
        backend = get_backend(info.context, provider, **kwargs)
        return cls(result=backend.start())


class AbstractSocialAuthCompleteMutation(graphene.Mutation):

    class Meta:
        abstract = True

    class Arguments: 
        requestData = graphene.JSONString(default_value={})
        provider = graphene.String(required=True)
        redirectUri = graphene.String(required=True)

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
        backend = get_backend(info.context, provider, **kwargs)
        backend.REDIRECT_STATE = False
        backend.STATE_PARAMETER = False
        backend.redirect_uri = kwargs.get('redirectUri')
      
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
        is_new = False
        
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


               
class AbstractSocialAuthDisconnectMutation(graphene.Mutation):

    class Meta:
        abstract = True

    class Arguments:
        requestData = graphene.JSONString(default_value={})
        provider = graphene.String(required=True)

    @classmethod
    def get_result(cls,
            backend,
            user,
            is_disconnected,
            **kwargs):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def mutate(cls, root, info, provider, **kwargs):
        backend = get_backend(info.context, provider, **kwargs)
        user = info.context.user

        is_disconnected = False

        partial = partial_pipeline_data(backend, user, *args, **kwargs)
        if partial:
            if association_id and not partial.kwargs.get('association_id'):
                partial.extend_kwargs({
                    'association_id': association_id
                })
            response = backend.disconnect(*partial.args, **partial.kwargs)
            # clean partial data after usage
            backend.strategy.clean_partial_pipeline(partial.token)
        else:
            response = backend.disconnect(user=user, association_id=association_id,
                                          *args, **kwargs)

        if isinstance(response, dict):
            is_disconnected = True
        else:
            return response

        return cls(result=cls.get_result(backend, user, is_disconnected))


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

class SocialAuthDisconnect(AbstractSocialAuthDisconnectMutation):
    """Social Auth Mutation"""

    result = graphene.Field(results.SocialAuthDisconnectResult)

    @classmethod
    def get_result(cls,
            backend,
            user,
            is_disconnected,
            **kwargs):
        return results.Disconnect(is_disconnected=is_disconnected)
