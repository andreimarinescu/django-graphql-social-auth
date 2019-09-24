import graphene
from . import types


class Social(graphene.ObjectType):
    social = graphene.Field(types.SocialType)

    is_successful_login = graphene.Boolean()
    is_inactive_user = graphene.Boolean()
    is_new = graphene.Boolean()
    is_new_association = graphene.Boolean()


class JWT(Social):
    token = graphene.String()


class Redirect(graphene.ObjectType):
    url = graphene.String(description='Redirect url')


class Html(graphene.ObjectType):
    content = graphene.String(description='Html content')


class SocialAuthResult(graphene.Union):
    class Meta:
        types = [Redirect, Html]


class SocialAuthCompleteResult(graphene.Union):
    class Meta:
        types = [Social, Redirect, Html]


class SocialAuthJWTCompleteResult(graphene.Union):
    class Meta:
        types = [JWT, Redirect, Html]
