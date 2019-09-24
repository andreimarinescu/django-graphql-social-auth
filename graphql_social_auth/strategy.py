from social_django.strategy import DjangoStrategy
from .results import Redirect, Html

class GraphqlStrategy(DjangoStrategy):

    def __init__(self, storage, request=None, tpl=None, providerData=None):
        self.providerData = providerData or {}
        super(GraphqlStrategy, self).__init__(storage, request, tpl)

    def redirect(self, url):
        return Redirect(url=url)

    def request_data(self, merge=True):
        data = super(GraphqlStrategy, self).request_data(merge)
        data.update(self.providerData)
        return data

    def html(self, content):
        return Html(content=content)
