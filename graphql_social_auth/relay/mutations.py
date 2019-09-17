import graphene

from . import nodes
from .. import mutations
from ..decorators import social_auth


class AbstractSocialAuthMutation(graphene.relay.ClientIDMutation):

    social = graphene.Field(nodes.SocialNode)

    class Meta:
        abstract = True

    class Input(mutations.SocialAuth.Arguments):
        """Social Auth Input"""


class SocialAuth(AbstractSocialAuthMutation):
    """Social Auth Mutation for Relay"""

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        return mutations.SocialAuth.mutate(root, info, **kwargs)


class SocialAuthJWT(AbstractSocialAuthMutation):
    """Social Auth for JSON Web Token (JWT)"""
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        return mutations.SocialAuthJWT.mutate(root, info, **kwargs)


