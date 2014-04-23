from django import template

from microdev.utils import render_template

import logging
logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def get_item(dictionary, key):
	"""
		A simple filter to provide dict key access.

		usage: {% my_dict|get_item:my_key %}
	"""
	return dictionary.get(key)


@register.filter
def lookup(d, key):
	"""
		A simpler filter to provide dict key access AND list indexing.

		usage: {% my_dict|get_item:my_key %}
	"""
	return d[key]


@register.filter
def show_errors(form):
	"""
		Displays form errors using the template specified.
	"""
	context_dict = {
		'form': form,
	}
	return render_template("microdev/show_errors.html", context_dict)


@register.filter
def get_range( value ):
	"""
		Returns a standard Python zero-based range.

		from: https://djangosnippets.org/snippets/1357/

		Filter - returns a list containing range made from given value
		Usage (in template):

		<ul>
			{% for i in 3|get_range %}
				<li>{{ i }}. Do something</li>
			{% endfor %}
		</ul>

		Results with the HTML:
		<ul>
			<li>0. Do something</li>
			<li>1. Do something</li>
			<li>2. Do something</li>
		</ul>

		Instead of 3 one may use the variable set in the views
	"""
	return range( value )


@register.filter
def get_range0( value ):
	""" 
		Convenience filter to make range numbering explicit to avoid
		any confusion. Also matches Django's forloop.counter0 
		convention.
	"""
	return get_range(value)


@register.filter
def get_range1( value ):
	"""
		Same as get_range but with a 1-based range, end inclusive.

		<ul>
			{% for i in 3|get_range1 %}
				<li>{{ i }}. Do something</li>
			{% endfor %}
		</ul>

		Results with the HTML:
		<ul>
			<li>1. Do something</li>
			<li>2. Do something</li>
			<li>3. Do something</li>
		</ul>
	"""
	return range( 1, int(value)+1 )


@register.filter(is_safe=True)
def floatformat_minmax(text, args='1,3'):
	"""
	Displays a float to a specified number of decimal places.

	* num1 = 34.23234
	* num2 = 34.00000
	* num3 = 34.26000
	* {{ num1|floatformat_minmax:'1,3' }} displays "34.232"
	* {{ num2|floatformat_minmax:'1,3' }} displays "34.0"
	* {{ num3|floatformat_minmax:'1,3' }} displays "34.26"
	"""
	import six
	from decimal import Decimal, InvalidOperation, Context, ROUND_HALF_UP
	from django.template.defaultfilters import special_floats
	from django.utils.encoding import force_text
	from django.utils import formats
	from django.utils.safestring import mark_safe

	arg_list = [int(arg) for arg in args.split(',')]

	min_digits = arg_list[0]
	max_digits = arg_list[1]

	try:
		input_val = force_text(text)
		d = Decimal(input_val)
	except UnicodeEncodeError:
		return ''
	except InvalidOperation:
		if input_val in special_floats:
			return input_val
		try:
			d = Decimal(force_text(float(text)))
		except (ValueError, InvalidOperation, TypeError, UnicodeEncodeError):
			return ''
	try:
		p = int(max_digits)
	except ValueError:
		return input_val

	try:
		m = int(d) - d
	except (ValueError, OverflowError, InvalidOperation):
		return input_val

	if not m and p < 0:
		return mark_safe(formats.number_format('%d' % (int(d)), 0))

	if p == 0:
		exp = Decimal(1)
	else:
		exp = Decimal('1.0') / (Decimal(10) ** abs(p))
	try:
		# Set the precision high enough to avoid an exception, see #15789.
		tupl = d.as_tuple()
		units = len(tupl[1]) - tupl[2]
		prec = abs(p) + units + 1

		# Avoid conversion to scientific notation by accessing `sign`, `digits`
		# and `exponent` from `Decimal.as_tuple()` directly.
		sign, digits, exponent = d.quantize(exp, ROUND_HALF_UP,
			Context(prec=prec)).as_tuple()
		digits = [six.text_type(digit) for digit in reversed(digits)]
		while len(digits) <= abs(exponent):
			digits.append('0')
		digits.insert(-exponent, '.')
		if sign:
			digits.append('-')
		number = ''.join(reversed(digits))
		number_str = formats.number_format(number, abs(p))

		decimal_splits = number_str.rsplit('.')
		decimal_str = decimal_splits[1]
		while decimal_str[-1:] == '0' and len(decimal_str) > min_digits:
			decimal_str = decimal_str[0:(len(decimal_str)-1)]

		new_decimal_str = "%s.%s" % (decimal_splits[0], decimal_str)

		return mark_safe(new_decimal_str)
	except InvalidOperation:
		return input_val