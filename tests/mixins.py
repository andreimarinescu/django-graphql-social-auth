import sys
import json
from unittest.mock import patch

from .decorators import social_auth_mock


class SocialAuthMixin:

    @social_auth_mock
    def test_social_auth(self, *args):

        response = self.execute({
            'provider': 'google-oauth2'
        })
        self.assertIsNotNone(response.data['socialAuth']['result']['url'])


class SocialAuthCompleteMixin:

    @social_auth_mock
    def test_social_auth(self, *args):
        requestData = {
            'access_token': '-token-',
        }
        response = self.execute({
            'provider': 'google-oauth2',
            'requestData': json.dumps(requestData)
        })
        social = response.data['socialAuthComplete']['result']['social']
        self.assertEqual('test', social['uid'])


class SocialAuthJWTCompleteMixin:

    @social_auth_mock
    def test_social_auth(self, *args):

        requestData = {
            'access_token': '-token-',
        }
        response = self.execute({
            'provider': 'google-oauth2',
            'requestData': json.dumps(requestData)
        })

        jwt = response.data['socialAuthComplete']['result']
        self.assertIsNotNone(jwt['token'])


    @social_auth_mock
    @patch.dict(sys.modules, {'graphql_jwt.shortcuts': None})
    def test_social_auth_import_error(self, *args):
        
        requestData = {
            'access_token': '-token-',
        }
        response = self.execute({
            'provider': 'google-oauth2',
            'requestData': json.dumps(requestData)
        })

        self.assertTrue(response.errors)
        self.assertIsNone(response.data['socialAuthComplete'])
