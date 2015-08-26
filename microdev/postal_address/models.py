from django.db import models
from django.utils.translation import ugettext as _


class PostalAddress(models.Model):
	country_code = models.CharField(max_length=3, default='US')

	class Meta:
		abstract = True


class AbstractUsPostalAddress(PostalAddress):
	"""
		Abstract base class. Use to directly add address fields to derived classes.
	"""
	address_line_1 = models.CharField(_("address line 1"), max_length=128, blank=True, null=True)
	address_line_2 = models.CharField(_("address line 2"), max_length=128, blank=True, null=True)

	city = models.CharField(_("city"), max_length=128, blank=True, null=True)
	state = models.CharField(_("state"), max_length=2, blank=True, null=True)
	zip_code = models.CharField(_("zip code"), max_length=5, blank=True, null=True)
	zip_plus_four = models.CharField(_("zip plus four"), max_length=4, blank=True, null=True)

	class Meta:
		abstract = True

	def __unicode__(self):
		if self.address_line_2:
			return "%s, %s, %s, %s %s" % (self.address_line_1, self.address_line_2, self.city, self.state, self.zip_code)
		else:
			return "%s, %s, %s %s" % (self.address_line_1, self.city, self.state, self.zip_code)


class UsPostalAddress(AbstractUsPostalAddress):
	"""
		Concrete class. Other objects will reference entries via FKs.
	"""
	pass
