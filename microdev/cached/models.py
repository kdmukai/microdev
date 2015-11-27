from django.db import models

from caching.base import CachingManager, CachingMixin

import os

try:
	import memcache
	memcache_available = True
except ImportError:
	memcache_available = False

if os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine') or os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
	is_appengine = True
else:
	is_appengine = False


if is_appengine or (not is_appengine and memcache_available):
	"""
		Google App Engine version to allow for script support when there's no memcache
		environment running.
	"""
	class CachedModel(models.Model, CachingMixin):
		objects = CachingManager()

		class Meta:
			abstract = True

else:
	class CachedModel(models.Model):
		""" 
			Disables model caching when there is no memcache environment.
		"""
		class Meta:
			abstract = True
