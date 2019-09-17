import graphene
from graphene import relay
from social_django import models as social_models

from .. import results

class Partial(results.Partial):
	class Meta:
		interfaces = [relay.Node]

class Social(results.Social):
	class Meta:
		interfaces = [relay.Node]

class JWT(Social):
	class Meta:
		interfaces = [relay.Node]

class SocialAuthResult(graphene.Union):
    class Meta:
        types = [Partial, Social]

class SocialAuthJWTResult(graphene.Union):
    class Meta:
        types = [Partial, JWT]

class SocialAuthResultConnection(graphene.Connection):
    class Meta:
        node = SocialAuthResult

class SocialAuthJWTResultConnection(graphene.Connection):
    class Meta:
        node = SocialAuthJWTResult

