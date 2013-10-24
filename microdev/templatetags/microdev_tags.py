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
