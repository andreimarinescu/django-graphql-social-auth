import graphene
from graphene import relay
from social_django import models as social_models

from .. import results

class SocialAuthResultNode(results.SocialAuthesult):

    class Meta:
        interfaces = [relay.Node]


class SocialAuthCompleteResultNode(results.SocialAuthCompleteResult):

    class Meta:
        interfaces = [relay.Node]


class SocialAuthJWTCompleteResultNode(results.SocialAuthJWTCompleteResult):

    class Meta:
        interfaces = [relay.Node]

