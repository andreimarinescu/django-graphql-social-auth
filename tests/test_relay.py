import graphene

import graphql_social_auth

from . import mixins
from .testcases import RelaySchemaTestCase


class SocialAuthTests(mixins.SocialAuthCompleteMixin, RelaySchemaTestCase):
    query = '''
    mutation SocialAuthComplete($input: SocialAuthCompleteInput!) {
      socialAuthComplete(input: $input) {
        result {
          __typename
          ... on Social {
            social {
              uid
              extraData
            }
          }
        }
        clientMutationId
      }
    }'''

    class Mutations(graphene.ObjectType):
        social_auth_complete = graphql_social_auth.relay.SocialAuthComplete.Field()


class SocialAuthJWTTests(mixins.SocialAuthJWTCompleteMixin,
                         RelaySchemaTestCase):

    query = '''
    mutation SocialAuthComplete($input: SocialAuthJWTCompleteInput!) {
      socialAuthComplete(input: $input) {
        result {
          __typename
          ... on JWT {
            social {
              uid
              extraData
            }
            token
          }
        }
        clientMutationId
      }
    }'''

    class Mutations(graphene.ObjectType):
        social_auth_complete = graphql_social_auth.relay.SocialAuthJWTComplete.Field()
