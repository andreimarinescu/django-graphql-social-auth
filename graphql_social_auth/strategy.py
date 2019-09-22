from social_django.strategy import DjangoStrategy
from .results import Redirect, Html

class GraphqlStrategy(DjangoStrategy):

    def __init__(self, storage, request=None, tpl=None, provider_data=None):
        super(GraphqlStrategy, self).__init__(storage, request, tpl)
        self.provider_data = provider_data or {}

    def redirect(self, url):
        return Redirect(url=url, session=self.session)

    def request_data(self, merge=True):
        data = super(GraphqlStrategy, self).__init__(self, merge=merge)
        data.update(self.provider_data)
        return data

    def html(self, content):
        return Html(content=content, session=self.session)
