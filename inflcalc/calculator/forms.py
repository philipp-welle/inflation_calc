from django import forms
import re
from django_countries.fields import CountryField
from crispy_forms.helper import FormHelper


class CommonFormHelpers:
    # don't show labels
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    # validate the user input
    def validate_year(self, year):
        if not re.match(r'^\d{4}$', year):
            raise forms.ValidationError("Enter a valid year in the format YYYY.")
        elif int(year) < 1980:
            raise forms.ValidationError("The earliest year is 1980")
        elif int(year) > 2022:
            raise forms.ValidationError("Please pick a year before 2023")
        return year


class UpdateLengthForm(CommonFormHelpers, forms.Form):
    starting_date = forms.CharField(max_length=4, required=False, widget=forms.TextInput(attrs={'placeholder': 'change start year'}))

    def clean_starting_date(self):
        year = self.cleaned_data['starting_date']
        self.validate_year(year)
        return year


class SetStartDate(CommonFormHelpers, forms.Form):
    country = CountryField(blank_label='(select country)', max_length=50).formfield()
    year = forms.CharField(max_length=4, required=True, widget=forms.TextInput(attrs={'placeholder': 'year'}))

    def clean_year(self):
        year = self.cleaned_data['year']
        self.validate_year(year)
        return year


class CalcForm(forms.Form):
    salary = forms.CharField(required=False)
    def validate_number(self, salary):
        if isinstance(salary, str):
            raise forms.ValidationError("Please enter a number")
        return salary
