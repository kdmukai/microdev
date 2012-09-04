
"""--------------------------------------------------------------------------
    Convenience method to easily access Django's templating engine.
--------------------------------------------------------------------------"""
def render_template(template_name, context_dict):
    from django.template.loader import get_template
    from django.template import Context

    # User Django's template system to render the template
    context = Context(context_dict)
    
    # Render and return as a string...
    return get_template(template_name).render(context)
