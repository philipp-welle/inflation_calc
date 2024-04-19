from django.shortcuts import render, redirect
from .forms import update_length_form, calcForm, set_start_date
from .inflation_data import Inflation
import pycountry
from currency_symbols import CurrencySymbols
from countryinfo import CountryInfo
import locale
locale.setlocale(locale.LC_ALL, '')

inflation = Inflation()

def landing(request):
    if request.method == "POST":
        form = set_start_date(request.POST)
        if form.is_valid():
            inflation.start_year = int(form.cleaned_data["year"])
            alpha_2_country = form.cleaned_data["country"]
            inflation.country = pycountry.countries.get(alpha_2=alpha_2_country).alpha_3 # change alpha_2 country code to alpha_3
            inflation.country_name = pycountry.countries.get(alpha_2=alpha_2_country).name # set country name
            return redirect("calc")
        else:
            return render(request, "calculator/landing.html", {"form": form})
    else:
        form = set_start_date()
        return render(request, "calculator/landing.html", {"form": form})


def calc(request):
    inflation.get_data(inflation.start_year)
    years = list(inflation.modified_dict.keys())[::-1]
    percent = [value[2] for value in inflation.modified_dict.values()][::-1]
    inflation_percent = [f"{value[0]}%" for value in inflation.modified_dict.values()][::-1]
    country_name = inflation.country_name
    currency = CountryInfo(country_name).currencies()[0] # currency code
    currency_symbol = CurrencySymbols.get_symbol(currency) # super complicated way to get currency symbol based on country code
    inflated = [0] * len(years)
    salaries = [0] * len(years)
    if request.method == "POST":
        form_a = update_length_form(request.POST)
        form_b = calcForm(request.POST)

        if form_b.is_valid():
            # extract salaries from post data
            salaries = [float(request.POST.get(f"salaries_{year}")) or 0 for year in years]
            # calculate inflated salaries and format it to currency
            inflated = [f"{currency_symbol}{'{:0,.2f}'.format(round(salary * (percentage / 100), 2))}" for salary, percentage in zip(salaries, percent)]
            table_data = zip(years, percent, salaries, inflated, inflation_percent)
            return render(request, "calculator/home.html",
                          {"form_a": form_a, "form_b": form_b, "table_data": table_data, "percent": percent, "country_name": country_name})
    else:
        form_a = update_length_form()
        form_b = calcForm()
    table_data = zip(years, percent, salaries, inflated, inflation_percent)

    return render(request, "calculator/home.html",
                  {"form_a": form_a, "form_b": form_b, "table_data": table_data, "percent": percent, "country_name": country_name})

def update_length(request):
    if request.method == 'POST':
        form_a = update_length_form(request.POST)
        # TODO clean this to reuse existing input
        if form_a.is_valid():
            starting_date = int(form_a.cleaned_data["starting_date"])
            inflation.get_data(starting_date)
            years = list(inflation.modified_dict.keys())[::-1]
            percent = [value[2] for value in inflation.modified_dict.values()][::-1]
            inflation_percent = [f"{value[0]}%" for value in inflation.modified_dict.values()][::-1]
            country_name = inflation.country_name
            inflated = [0] * len(years)
            salaries = [0] * len(years)
            table_data = zip(years, percent, salaries, inflated, inflation_percent)
            return render(request, "calculator/home.html", {"form_a": form_a, "table_data": table_data, "percent": percent, "country_name": country_name})
        else:
            # TODO check to see if we still need this
            years = list(inflation.modified_dict.keys())[::-1]
            percent = [value[2] for value in inflation.modified_dict.values()][::-1]
            inflation_percent = [f"{value[0]}%" for value in inflation.modified_dict.values()][::-1]
            country_name = inflation.country_name
            inflated = [0] * len(years)
            salaries = [0] * len(years)
            table_data = zip(years, percent, salaries, inflated, inflation_percent)
            return render(request, "calculator/home.html", {"form_a": form_a, "table_data": table_data, "percent": percent, "country_name": country_name})

#TODO BUG set year - update year - goes back to first set year when calculate