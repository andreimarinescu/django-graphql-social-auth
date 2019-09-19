import graphene
from graphene import relay
from social_django import models as social_models

from .. import mutations

from .. import results

class SocialAuthResultNode(mutations.SocialAuthResult):
    class Meta:
        types = [results.Redirect, results.Social]
        interfaces = [relay.Node]

class SocialAuthJWTResultNode(mutations.SocialAuthJWTResult):
    class Meta:
        types = [results.Redirect, results.JWT]
        interfaces = [relay.Node]

class SocialAuth(mutations.SocialAuth):
    
    results = graphene.Field(SocialAuthResultNode)

    class Meta:
        interfaces = [relay.Node]

class SocialAuthJWT(mutations.SocialAuthJWT):
    
    results = graphene.Field(SocialAuthJWTResultNode)

    class Meta:
        interfaces = [relay.Node]
