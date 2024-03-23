from django import forms
import re


class update_length_form(forms.Form):
    starting_date = forms.CharField(label="Starting year", max_length=4, required=False)

    def clean_starting_date(self):
        starting_date = self.cleaned_data['starting_date']
        if not re.match(r'^\d{4}$', starting_date):
            raise forms.ValidationError("Enter a valid year in the format YYYY.")
        elif int(starting_date) < 1980:
            raise forms.ValidationError("The earliest year is 1980")
        elif int(starting_date) > 2022:
            raise forms.ValidationError("Please pick a year before 2023")
        return starting_date


class calcForm(forms.Form):
    # Define fields for form_a here
    #field_a = forms.CharField(label='Field A', max_length=100)
    pass