from django.forms import ModelForm
from postal_address.models import UsPostalAddress
from localflavor.us.forms import USStateField
from localflavor.us.us_states import STATE_CHOICES
from django import forms

class UsPostalAddressForm(ModelForm):
    US_STATE_CHOICES = list(STATE_CHOICES)
    US_STATE_CHOICES.insert(0, ('', '---------'))
    state = USStateField(widget=forms.Select(
            choices=US_STATE_CHOICES))
    
    class Meta:
        model = UsPostalAddress
        exclude = ('country_code',)
