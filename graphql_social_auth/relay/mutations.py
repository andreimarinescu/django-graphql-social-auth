import graphene

from . import nodes
from .. import mutations


class SocialAuth(graphene.relay.ClientIDMutation):
    
    results = graphene.Field(SocialAuthResultNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        return mutations.SocialAuth.mutate(root, info, **kwargs)


class SocialAuthComplete(graphene.relay.ClientIDMutation):
    
    results = graphene.Field(SocialAuthCompleteResultNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        return mutations.SocialAuthComplete.mutate(root, info, **kwargs)


class SocialAuthJWTComplete(graphene.relay.ClientIDMutation):
    
    results = graphene.Field(SocialAuthJWTCompleteResultNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        return mutations.SocialAuthJWTComplete.mutate(root, info, **kwargs)
