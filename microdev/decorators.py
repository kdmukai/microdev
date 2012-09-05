from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.utils.decorators import available_attrs
from functools import wraps

from microdev import POST_LOGIN_REDIR_PARAM


"""--------------------------------------------------------------------------
    Stores the current url in the session so that it can be retrieved after a 
    third-party oauth login (e.g. login with Facebook). Then calls the normal 
    login_required decorator.
    
    km: I'll be honest; I barely understand decorators and function wrapping.
    It's working as expected but only because of a ton of trial-and-error.
--------------------------------------------------------------------------"""
def login_required_with_session_redirect(function=None, redirect_field_name=None, login_url=None):
    print('login_required_with_session_redirect')

    def add_redir_param(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            print('add_redir_param')
            request.session[POST_LOGIN_REDIR_PARAM] = request.path
            
            print('set post_login_redir_url: ' + request.session[POST_LOGIN_REDIR_PARAM])
            return function(request, *args, **kwargs)
        return wrapper


    if function:
        return add_redir_param(login_required(function))
    else:
        return add_redir_param(login_required)
