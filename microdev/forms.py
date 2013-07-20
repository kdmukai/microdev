from django import forms
from django.utils.translation import gettext


"""--------------------------------------------------------------------------
    A trivial Form to handle simple checkbox confirmation pages. DRY, right?
--------------------------------------------------------------------------"""
class ConfirmCheckboxForm(forms.Form):
    confirm = forms.BooleanField(required=True, label=gettext('Confirm checkbox'))


"""--------------------------------------------------------------------------
    A trivial Form to handle simple email entry pages. DRY, right?
--------------------------------------------------------------------------"""
class EmailForm(forms.Form):
    email = forms.EmailField(required=True)