import graphene


from django.utils.translation import ugettext_lazy as _

from social_core.exceptions import MissingBackend
from .utils import load_backend, load_strategy
from social_django.views import _do_login

from . import exceptions, results, partial

class AbstractSocialAuth(graphene.Union):
    class Meta:
        abstract = True

class SocialAuthResult(graphene.Union):
    class Meta:
        types = [results.Redirect, results.Social]

class SocialAuthJWTResult(graphene.Union):
    class Meta:
        types = [results.Redirect, results.JWT]
        
class AbstractSocialAuthMutation(graphene.Mutation):

    class Meta:
        abstract = True

    class Arguments:
        provider = graphene.String(required=True)
        access_token = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, provider, access_token, **kwargs):
        strategy = load_strategy(info.context)

        try:
            backend = load_backend(strategy, provider, redirect_uri=None)
        except MissingBackend:
            raise exceptions.GraphQLSocialAuthError(_('Provider not found'))

        if info.context.user.is_authenticated:
            authenticated_user = info.context.user
        else:
            authenticated_user = None

        user_or_result = backend.do_auth(access_token, user=authenticated_user)

        if user_or_result  is None:
            raise exceptions.InvalidTokenError(_('Invalid token'))

        user_model = strategy.storage.user.user_model()

        if isinstance(user_or_result, graphene.ObjectType):
            return user_or_result

        elif not isinstance(user_or_result, user_model):
            msg = _('`{}` is not a user or graphene.ObjectType instance').format(type(user_or_result).__name__)
            raise exceptions.DoAuthError(msg, user_or_result)

        return cls(result=cls.get_loginresult(backend, user_or_result))

class SocialAuth(AbstractSocialAuthMutation):
    """Social Auth Mutation"""

    result = graphene.Field(SocialAuthResult)

    Social = results.Social

    @classmethod
    def get_loginresult(cls, backend, user):
        _do_login(backend, user, user.social_user)
        return cls.Social(social=user.social_user)


class SocialAuthJWT(AbstractSocialAuthMutation):
    """Social Auth for JSON Web Token (JWT)"""

    result = graphene.Field(SocialAuthJWTResult)

    Social = results.JWT

    @classmethod
    def get_loginresult(cls, backend, user):
        try:
            from graphql_jwt.shortcuts import get_token
        except ImportError:
            raise ImportError(
                'django-graphql-jwt not installed.\n'
                'Use `pip install \'django-graphql-social-auth[jwt]\'`.')
        return cls.Social(social=user.social_user, token=get_token(user))
