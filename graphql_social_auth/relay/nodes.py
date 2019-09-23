import graphene
from graphene import relay
from social_django import models as social_models

from .. import results

class SocialAuthResultNode(results.SocialAuthResult):

    class Meta:
        types = results.SocialAuthResult._meta.types
        interfaces = [relay.Node]


class SocialAuthCompleteResultNode(results.SocialAuthCompleteResult):

    class Meta:
        types = results.SocialAuthCompleteResult._meta.types
        interfaces = [relay.Node]


class SocialAuthJWTCompleteResultNode(results.SocialAuthJWTCompleteResult):

    class Meta:
        types = results.SocialAuthJWTCompleteResult._meta.types
        interfaces = [relay.Node]

