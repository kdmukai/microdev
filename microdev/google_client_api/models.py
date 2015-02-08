from django.db import models

from oauth2client.django_orm import CredentialsField

from south.modelsinspector import add_introspection_rules


# class ServerCredentialsManager(models.Manager):


# Required so South can "freeze" the field properly. See:
#	http://south.aeracode.org/wiki/MyFieldsDontWork
add_introspection_rules([], ["^oauth2client\.django_orm\.CredentialsField"])

class ServerCredentials(models.Model):
	"""
		Use the normal web-based client authorization method to enable server-to-server
		Google API calls (e.g. Drive) without the added mechanism of a dedicated
		Service Account.

		This way local dev doesn't have to be any different from Production.
	"""
	credentials = CredentialsField()

