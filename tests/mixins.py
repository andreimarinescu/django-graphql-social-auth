import sys
import json
from unittest.mock import patch

from .decorators import social_auth_mock


class SocialAuthCompleteMixin:

    @social_auth_mock
    def test_social_auth(self, *args):
        providerData = {
            'access_token': '-token-',
        }
        response = self.execute({
            'provider': 'google-oauth2',
            'providerData': json.dumps(providerData)
        })
        print(response.errors)
        social = response.data['socialAuthComplete']['result']['social']
        self.assertEqual('test', social['uid'])


class SocialAuthJWTCompleteMixin:

    @social_auth_mock
    def test_social_auth(self, *args):

        providerData = {
            'access_token': '-token-',
        }
        response = self.execute({
            'provider': 'google-oauth2',
            'providerData': json.dumps(providerData)
        })

        jwt = response.data['socialAuthComplete']['result']
        self.assertIsNotNone(jwt['token'])


    @social_auth_mock
    @patch.dict(sys.modules, {'graphql_jwt.shortcuts': None})
    def test_social_auth_import_error(self, *args):
        
        providerData = {
            'access_token': '-token-',
        }
        response = self.execute({
            'provider': 'google-oauth2',
            'providerData': json.dumps(providerData)
        })

        self.assertTrue(response.errors)
        self.assertIsNone(response.data['socialAuthComplete'])
