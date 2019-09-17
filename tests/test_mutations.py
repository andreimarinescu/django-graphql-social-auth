import graphene

import graphql_social_auth

from . import mixins
from .testcases import SchemaTestCase


class SocialAuthTests(mixins.SocialAuthMixin, SchemaTestCase):
    query = '''
    mutation SocialAuth($provider: String!, $accessToken: String!) {
      socialAuth(provider: $provider, accessToken: $accessToken) {
        result {
          __typename
          ... on Social {
            social {
              uid
              extraData
            }
          }
        }
      }
    }'''

    class Mutations(graphene.ObjectType):
        social_auth = graphql_social_auth.SocialAuth.Field()


class SocialAuthJWTTests(mixins.SocialAuthJWTMixin,
                         SchemaTestCase):

    query = '''
    mutation SocialAuth($provider: String!, $accessToken: String!) {
      socialAuth(provider: $provider, accessToken: $accessToken) {
        result {
          __typename
          ... on JWT {
             token
          }
        }
      }
    }'''

    class Mutations(graphene.ObjectType):
        social_auth = graphql_social_auth.SocialAuthJWT.Field()
