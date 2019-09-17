import graphene
from . import types

class PartialResult(graphene.ObjectType):
    partial = graphene.Field(types.Partial)

class SocialResult(graphene.ObjectType):
    social = graphene.Field(types.Social)

class JWTResult(SocialResult):
    token = graphene.String()
