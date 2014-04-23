from django.db import models

from caching.base import CachingManager, CachingMixin


"""
	Google App Engine version to allow for script support when there's no memcache
	environment running.
"""
import os
if os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine') or os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
	class CachedModel(models.Model, CachingMixin):
		objects = CachingManager()

		class Meta:
			abstract = True
else:
	class CachedModel(models.Model):
		""" 
			Uncomment this version to enable shell execution when there is
			no memcache environment.
		"""
		class Meta:
			abstract = True
