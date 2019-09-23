import graphene

import graphql_social_auth

from . import mixins
from .testcases import SchemaTestCase


class SocialAuthCompleteTests(mixins.SocialAuthCompleteMixin, SchemaTestCase):
    query = '''
    mutation SocialAuthComplete($provider: String!, $providerData: JSONString!) {
      socialAuthComplete(provider: $provider, providerData: $providerData) {
        result {
          __typename
          ... on Social {
            social {
              uid
              extraData
            }
            isSuccessfulLogin
            isInactiveUser
            isNew
            isNewAssociation
          }
        }
      }
    }'''

    class Mutations(graphene.ObjectType):
        social_auth_complete = graphql_social_auth.SocialAuthComplete.Field()


class SocialAuthJWTCompleteTests(mixins.SocialAuthJWTCompleteMixin,
                         SchemaTestCase):

    query = '''
    mutation SocialAuthComplete($provider: String!, $providerData: JSONString!) {
      socialAuthComplete(provider: $provider, providerData: $providerData) {
        result {
          __typename
          ... on JWT {
            social {
              uid
              extraData
            }
            token
            isSuccessfulLogin
            isInactiveUser
            isNew
            isNewAssociation
          }
        }
      }
    }'''

    class Mutations(graphene.ObjectType):
        social_auth_complete = graphql_social_auth.SocialAuthJWTComplete.Field()
