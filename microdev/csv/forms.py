from django import forms

"""--------------------------------------------------------------------------
    A trivial Form to handle simple CSV File upload pages. DRY, right?
--------------------------------------------------------------------------"""
class CsvFileForm(forms.Form):
	file = forms.FileField(
		required=True,
        label='Select a CSV file.'
    )
	has_header_row = forms.BooleanField(initial=True)
