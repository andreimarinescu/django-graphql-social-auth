from unittest.mock import patch


def social_auth_mock(f):
    @patch('social_core.backends.base.BaseAuth.get_json')
    @patch('social_core.backends.oauth.OAuthAuth.validate_state')
    @patch('social_core.backends.oauth.BaseOAuth2.request_access_token')
    @patch('social_core.backends.google.BaseGoogleAuth.get_user_id')
    def wrapper(self, get_user_id_mock, request_access_token_mock, validate_state_mock, *args):
        get_user_id_mock.return_value = 'test' 
        validate_state_mock.return_value = 'state'
        request_access_token_mock.return_value = {'access_token': '-token-'}
        return f(self, get_user_id_mock, validate_state_mock, request_access_token_mock, *args)
    return wrapper
