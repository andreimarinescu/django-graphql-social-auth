from unittest.mock import patch

from django.test import override_settings

import graphene

from graphql_social_auth import exceptions
from graphql_social_auth import mutations

from .testcases import TestCase

from .decorators import social_auth_mock


class ExceptionsTests(TestCase):

    @social_auth_mock
    def test_psa_missing_backend(self, *args):

        with self.assertRaises(exceptions.GraphQLSocialAuthError):
            mutations.SocialAuth.mutate(None, self.info(), 'unknown', 'token')
            
    @social_auth_mock
    @override_settings(SOCIAL_AUTH_PIPELINE=[])
    def test_psa_invalid_token(self, *args):

        with self.assertRaises(exceptions.InvalidTokenError):
            mutations.SocialAuth.mutate(None, self.info(), 'google-oauth2', 'token')

    @social_auth_mock
    @patch('social_core.backends.oauth.BaseOAuth2.do_auth')
    def test_psa_do_auth_error(self, *args):

        with self.assertRaises(exceptions.DoAuthError):
             mutations.SocialAuth.mutate(None, self.info(), 'google-oauth2', 'token')