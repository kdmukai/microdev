
"""--------------------------------------------------------------------------
    Convenience method to easily access Django's templating engine.
--------------------------------------------------------------------------"""
def render_template(template_name, context_dict):
    from django.template.loader import get_template
    from django.template import Context

    # Use Django's template system to render the template
    context = Context(context_dict)
    
    # Render and return as a string...
    return get_template(template_name).render(context)



"""--------------------------------------------------------------------------
    Access Google's free currency exchange API.

    Use the 3-char ISO currency codes to specify source and target currency.
    
    Usage:
    Convert $15.43USD to Euros:
    amt_in_euros = 15.43 * get_current_exchange_rate('USD', 'EUR')
--------------------------------------------------------------------------"""
def get_current_exchange_rate(src_currency, tgt_currency):
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
