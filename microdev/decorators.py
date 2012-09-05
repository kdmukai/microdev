from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.utils.decorators import available_attrs
from functools import wraps

from microdev import POST_LOGIN_REDIR_PARAM


"""--------------------------------------------------------------------------
    Stores the current url in the session so that it can be retrieved after a 
    third-party oauth login (e.g. login with Facebook). In these cases the 
    normal 'next' request param is lost in the oauth exchange whereas the
    session is persistent when the user returns from the oauth intermediate 
    flow.
    
    Decorator then calls the standard login_required decorator.
    
    km: I'll be honest; I barely understand decorators and function wrapping.
    It's working as expected but only because of a ton of trial-and-error.
--------------------------------------------------------------------------"""
def login_required_with_session_redirect(function=None, redirect_field_name=None, login_url=None):

    def add_redir_param(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            # Store the current URL in the session
            request.session[POST_LOGIN_REDIR_PARAM] = request.path
            
            # We're done here. Let the incoming function execute
            return function(request, *args, **kwargs)
        return wrapper

    # Call the decorator's method and then relinquish control to login_required
    if function:
        return add_redir_param(login_required(function))
    else:
        # km: When would function be None?
        return add_redir_param(login_required)
