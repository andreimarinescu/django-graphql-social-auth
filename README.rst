Django GraphQL Social Auth
==========================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|

`Python Social Auth`_ support for `Django GraphQL`_

.. _Django GraphQL: https://github.com/graphql-python/graphene-django


Dependencies
------------

* Python ≥ 3.4
* Django ≥ 1.11


Installation
------------

Install last stable version from Pypi.

.. code:: sh

    pip install django-graphql-social-auth


See the `documentation`_ for further guidance on setting *Python Social Auth*.

.. _documentation: http://python-social-auth.readthedocs.io/en/latest/configuration/django.html

Add the ``SocialAuthComplete`` mutation to your GraphQL schema.

.. code:: python

    import graphene
    import graphql_social_auth


    class Mutations(graphene.ObjectType):
        social_auth = graphql_social_auth.SocialAuthComplete.Field()

`Session`_ authentication via *accessToken*.

.. _Session: https://docs.djangoproject.com/en/2.0/topics/http/sessions/

- ``provider``: provider name from `Authentication backend list`_.
- ``accessToken``: third-party (Google, Facebook...) OAuth token obtained with any OAuth client.

.. _Authentication backend list: https://github.com/flavors/django-graphql-social-auth/wiki/Authentication-backends

.. code:: graphql

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
    }

JSON Web Token (JWT)
--------------------

Authentication solution based on `JSON Web Token`_.

.. _JSON Web Token: https://jwt.io/

Install additional requirements.

.. code:: sh

    pip install 'django-graphql-social-auth[jwt]'


Add the ``SocialAuthJWTComplete`` mutation to your GraphQL schema.

.. code:: python

    import graphene
    import graphql_social_auth


    class Mutations(graphene.ObjectType):
        social_auth_complete = graphql_social_auth.SocialAuthJWTComplete.Field()


Authenticate via *accessToken* to obtain a JSON Web Token.

.. code:: graphql

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
    }


Relay
-----

Complete support for `Relay`_.

.. _Relay: https://facebook.github.io/relay/

.. code:: python

    import graphene
    import graphql_social_auth


    class Mutations(graphene.ObjectType):
        social_auth_complete = graphql_social_auth.relay.SocialAuthComplete.Field()

``graphql_social_auth.relay.SocialAuthJWTComplete.Field()`` for `JSON Web Token (JWT)`_ authentication.

`Relay mutations`_ only accepts one argument named *input*:

.. _Relay mutations: https://facebook.github.io/relay/graphql/mutations.htm

.. code:: graphql

    mutation SocialAuthComplete($provider: String!, $providerData: JSONString!) {
      socialAuthComplete(input:{provider: $provider, providerData: $providerData}) {
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
    }


Customizing
-----------

If you want to customize the ``SocialAuthComplete`` behavior, you'll need to customize the ``get_result()`` method on a subclass of ``SocialAuthComplete`` and add a new ``.relay.SocialAuthComplete`` for relay.

.. code:: python

    import graphene
    from graphql_social_auth import mutations, results

    class UserSocial(results.Social):
        user = graphene.Field(UserType)

        @classmethod
        def resolve_user(cls, root, info, **kwargs):
            return UserType(info.context.user)

    class SocialAuthCompleteResult(graphene.Union):
        class Meta:
            types = [UserSocial, results.Redirect, results.Html]
            
    class SocialAuthComplete(mutations.SocialAuthCompleteMutation):

        result = graphene.Field(SocialAuthCompleteResult)

        @classmethod
        def get_result(cls,
                  backend,
                  user,
                  is_successful_login,
                  is_inactive_user,
                  is_new,
                  is_new_association,
                  **kwargs):
            return UserSocial(user=user,
                social=user.social_user,
                is_successful_login = is_successful_login,
                is_inactive_user = is_inactive_user,
                is_new = is_new,
                is_new_association = is_new_association,
                session = backend.strategy.session)


Authenticate via *accessToken* to obtain the *user id*.

.. code:: graphql

    mutation SocialAuthComplete($provider: String!, $providerData: JSONString!) {
      socialAuthComplete(provider: $provider, providerData: $providerData) {
        result {
          __typename
          ... on UserSocial {
            social {
              uid
              extraData
            }
            user {
              id
            }
            isSuccessfulLogin
            isInactiveUser
            isNew
            isNewAssociation
          }
        }
      }
    }


.. Project template
.. ----------------

.. There is a `Django project template`_ to start a demo project.

.. .. _Django project template: https://github.com/ice-creams/graphql-social-auth-template

----

Gracias `@omab`_ / `Python Social Auth`_.

.. _@omab: https://github.com/omab
.. _Python Social Auth: http://python-social-auth.readthedocs.io/


.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-social-auth.svg
   :target: https://pypi.python.org/pypi/django-graphql-social-auth

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-graphql-social-auth.svg
   :target: https://pypi.python.org/pypi/django-graphql-social-auth

.. |Build Status| image:: https://travis-ci.org/flavors/django-graphql-social-auth.svg?branch=master
   :target: https://travis-ci.org/flavors/django-graphql-social-auth

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/django-graphql-social-auth.svg
   :target: https://codecov.io/gh/flavors/django-graphql-social-auth

.. |Code Climate| image:: https://api.codeclimate.com/v1/badges/c579bcfde0fbb7f6334c/maintainability
   :target: https://codeclimate.com/github/flavors/django-graphql-social-auth
