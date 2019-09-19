from social_django.strategy import DjangoStrategy
from .results import Redirect

class GraphqlStrategy(DjangoStrategy):
	def redirect(self, url):
		return Redirect(url=url)