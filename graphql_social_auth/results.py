import graphene
from . import types

class Social(graphene.ObjectType):
    social = graphene.Field(types.SocialType)

class JWT(Social):
    token = graphene.String()

class Redirect(graphene.ObjectType):
    url = graphene.String(description='Redirect url')
