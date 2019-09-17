import graphene
from . import types

class Partial(graphene.ObjectType):
    partial = graphene.Field(types.PartialType)

class Social(graphene.ObjectType):
    social = graphene.Field(types.SocialType)

class JWT(Social):
    token = graphene.String()
