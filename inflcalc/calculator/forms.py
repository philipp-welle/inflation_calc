from django import forms
import re
from django_countries.fields import CountryField
from crispy_forms.helper import FormHelper


class update_length_form(forms.Form):
    def __init__(self, *args, **kwargs):
        super(update_length_form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    starting_date = forms.CharField(max_length=4, required=True, widget=forms.TextInput(attrs={'placeholder': 'year'}))

    def clean_starting_date(self):
        starting_date = self.cleaned_data['starting_date']
        if not re.match(r'^\d{4}$', starting_date):
            raise forms.ValidationError("Enter a valid year in the format YYYY.")
        elif int(starting_date) < 1980:
            raise forms.ValidationError("The earliest year is 1980")
        elif int(starting_date) > 2022:
            raise forms.ValidationError("Please pick a year before 2023")
        return starting_date

class set_start_date(forms.Form):
    def __init__(self, *args, **kwargs):
        super(set_start_date, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    country = CountryField(blank_label='(select country)', max_length=50).formfield()
    year = forms.CharField(max_length=4, required=True, widget=forms.TextInput(attrs={'placeholder': 'year'}))

    def clean_year(self):
        year = self.cleaned_data['year']
        if not re.match(r'^\d{4}$', year):
            raise forms.ValidationError("Enter a valid year in the format YYYY.")
        elif int(year) < 1980:
            raise forms.ValidationError("The earliest year is 1980")
        elif int(year) > 2022:
            raise forms.ValidationError("Please pick a year before 2023")
        return year


class calcForm(forms.Form):
    pass