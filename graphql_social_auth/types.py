from graphene_django.types import DjangoObjectType
from social_django import models as social_models

class SocialType(DjangoObjectType):

    class Meta:
        model = social_models.UserSocialAuth

    def resolve_extra_data(self, info, **kwargs):
        self.extra_data.pop('access_token', None)
        return self.extra_data

class PartialType(DjangoObjectType):

    class Meta:
        model = social_models.Partial

    def resolve_data(self, info, **kwargs):
        self.data.pop('token', None)
        return self.data
