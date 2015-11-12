import logging
default_logger = logging.getLogger(__name__)


def md5_hash_encode(cleartext):
	"""
		MD5 any arbitrary input. Returns the 16-digit hexidecimal hash as a 32-char string.
		e.g. md5_hash_encode("Hello, world!") = '6cd3556deb0da54bca060b4c39479839'
	"""
	from Crypto.Hash import MD5
	return MD5.new(cleartext).hexdigest()


def render_template(template_name, context_dict):
	"""
		Convenience method to easily access Django's templating engine.
	"""
	from django.template.loader import get_template
	from django.template import Context

	# Use Django's template system to render the template
	context = Context(context_dict)
	
	# Render and return as a string...
	return get_template(template_name).render(context)


def dump_post(request, logger=None):
	"""
		Just spits out every POST key and value in the request
		Specify optional logger to control output.
	"""
	for key in request.POST.keys():
		output_str = "%s: %s" % (key, request.POST[key])
		if logger:
			logger.debug(output_str)
		else:
			default_logger.debug(output_str)


def format_email_addressee(user):
	"""
		Takes an auth.User and outputs named email format "Jim Smith <jimsmith@blah.com>"
		when possible. Otherwise just returns email.

		Raw email instead of named format gets the attention of spam filters.
	"""
	if user.first_name and user.last_name:
		return "%s %s <%s>" % (user.first_name, user.last_name, user.email)

	elif user.first_name:
		return "%s %s <%s>" % (user.first_name, user.last_name, user.email)

	else:
		return user.email


def dump_post_str(request):
	"""
		Just spits out every POST key and value in the request
	"""
	output_str = ""
	for key in request.POST.keys():
		output_str += "%s: %s\n" % (key, request.POST[key])
	return output_str


def utc_to_localtime(utc_datetime, local_tz_name):
	"""
		Convert a TZ-aware datetime from UTC to the target named time zone

		utc_to_localtime(my_utc_datetime, 'America/Chicago')
	"""
	import pytz
	return utc_datetime.replace(tzinfo=pytz.utc).astimezone( pytz.timezone(local_tz_name) )


def get_current_exchange_rate(src_currency, tgt_currency):
	"""
		Access Google's free currency exchange API.

		Use the 3-char ISO currency codes to specify source and target currency.
		
		Usage:
		Convert $15.43USD to Euros:
		amt_in_euros = 15.43 * get_current_exchange_rate('USD', 'EUR')
	"""
	import urllib2

	response = urllib2.urlopen('http://www.google.com/ig/calculator?hl=en&q=1%s=?%s' % (src_currency, tgt_currency))
	data = response.read()
	
	# Returns hash: {lhs: "1 Euro",rhs: "1.3118 U.S. dollars",error: "",icc: true}
	print(data)

	index = data.find('rhs: "') + 6
	working_str = data[index:]
	print(working_str)
	exchange_rate, discard_remainder = working_str.split(' ', 1)
	print(exchange_rate)
	return float(exchange_rate)
