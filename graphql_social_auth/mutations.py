import graphene


from django.utils.translation import ugettext_lazy as _

from social_core.exceptions import MissingBackend
from social_django.utils import load_backend, load_strategy
from social_django.views import _do_login

from . import exceptions, results

class PartialResponse(object):
    response = None
    def __init__(response):
        self.response = response

class AbstractSocialAuthResult(graphene.Union):
    class Meta:
        abstract = True

    @staticmethod
    def resolve_type(obj, context, info):
        return obj.__class__

class SocialAuthResult(graphene.Union):
    class Meta:
        types = [results.PartialResult, results.SocialResult]

    @staticmethod
    def resolve_type(obj, context, info):
        return obj.__class__

class SocialAuthJWTResult(graphene.Union):
    class Meta:
        types = [results.PartialResult, results.JWTResult]

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

        user_or_partial = backend.do_auth(access_token, user=authenticated_user)

        if user_or_partial is None:
            raise exceptions.InvalidTokenError(_('Invalid token'))

        user_model = strategy.storage.user.user_model()

        if isinstance(user_or_partial, PartialResponse):
            return cls.classes().ResultUnion(
                result=cls.classes().PartialResult(
                    partial=user_or_partial.response)
                )

        elif not isinstance(user_or_partial, user_model):
            msg = _('`{}` is not a user instance').format(type(user_or_partial).__name__)
            raise exceptions.DoAuthError(msg, user_or_partial)

        return cls(result=cls.get_loginresult(backend, user_or_partial))

class SocialAuth(AbstractSocialAuthMutation):
    """Social Auth Mutation"""

    result = graphene.Field(SocialAuthResult)
    
    @classmethod
    def classes():
        return {
            SocialResult: results.SocialResult,
            PartialResult: results.PartialResult
        }

    @classmethod
    def get_loginresult(backend, user):
        _do_login(backend, user, user.social_user)
        return cls.classes().SocialResult(social=user.social_user)


class SocialAuthJWT(AbstractSocialAuthMutation):
    """Social Auth for JSON Web Token (JWT)"""

    result = graphene.Field(SocialAuthJWTResult)
    
    @classmethod
    def classes():
        return {
            SocialResult: results.JWTResult,
            PartialResult: results.PartialResult
        }


    @classmethod
    def get_loginresult(backend, user):
        try:
            from graphql_jwt.shortcuts import get_token
        except ImportError:
            raise ImportError(
                'django-graphql-jwt not installed.\n'
                'Use `pip install \'django-graphql-social-auth[jwt]\'`.')
        return cls.classes().JWTResult(social=user.social_user, token=get_token(user))
