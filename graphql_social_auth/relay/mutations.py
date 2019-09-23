import graphene

from . import nodes
from .. import mutations


class SocialAuth(graphene.relay.ClientIDMutation):
    
    result = graphene.Field(nodes.SocialAuthResultNode)

    class Input(mutations.SocialAuth.Arguments):
        """Social Auth Input"""

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        return mutations.SocialAuth.mutate(root, info, **kwargs)


class SocialAuthComplete(graphene.relay.ClientIDMutation):
    
    result = graphene.Field(nodes.SocialAuthCompleteResultNode)

    class Input(mutations.SocialAuthComplete.Arguments):
        """Social Auth Input"""

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        return mutations.SocialAuthComplete.mutate(root, info, **kwargs)


class SocialAuthJWTComplete(graphene.relay.ClientIDMutation):
    
    result = graphene.Field(nodes.SocialAuthJWTCompleteResultNode)

    class Input(mutations.SocialAuthJWTComplete.Arguments):
        """Social Auth Input"""
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        return mutations.SocialAuthJWTComplete.mutate(root, info, **kwargs)
