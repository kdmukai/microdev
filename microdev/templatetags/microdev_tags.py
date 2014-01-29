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
def get_range1( value ):
	"""
		Same as get_range but with 1-based range, end inclusive.

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
