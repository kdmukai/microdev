from django import forms
from django.utils.translation import gettext


"""--------------------------------------------------------------------------
    A trivial Form to handle simple checkbox confirmation pages. DRY, right?
--------------------------------------------------------------------------"""
class ConfirmCheckboxForm(forms.Form):
    confirm = forms.BooleanField(required=True, label=gettext('Confirm checkbox'))
