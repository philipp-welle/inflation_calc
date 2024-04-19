from django.shortcuts import render, redirect
from .forms import UpdateLengthForm, CalcForm, SetStartDate
from .inflation_data import Inflation
import pycountry
from currency_symbols import CurrencySymbols
from countryinfo import CountryInfo
import locale

locale.setlocale(locale.LC_ALL, '')

inflation = Inflation()


def landing(request):
    if request.method == "POST":
        form = SetStartDate(request.POST)
        if form.is_valid():
            inflation.start_year = int(form.cleaned_data["year"])
            alpha_2_country = form.cleaned_data["country"]
            inflation.country = pycountry.countries.get(
                alpha_2=alpha_2_country).alpha_3  # change alpha_2 country code to alpha_3
            inflation.country_name = pycountry.countries.get(alpha_2=alpha_2_country).name  # set country name
            return redirect("calc")
        else:
            return render(request, "calculator/landing.html", {"form": form})
    else: # needed for form validation
        form = SetStartDate()
        return render(request, "calculator/landing.html", {"form": form})


def calc(request):
    inflation.get_data(inflation.start_year)
    country_name = inflation.country_name
    currency = CountryInfo(country_name).currencies()[0]  # currency code
    currency_symbol = CurrencySymbols.get_symbol(
        currency)  # super complicated way to get currency symbol based on country code
    if request.method == "POST":
        form_a = UpdateLengthForm(request.POST)
        form_b = CalcForm(request.POST)
        if form_b.is_valid():
            # extract salaries from post data
            inflation.salaries = [float(request.POST.get(f"salaries_{year}")) or 0 for year in inflation.years]
            # calculate inflated salaries and format it to currency
            inflation.inflated = [f"{currency_symbol}{'{:0,.2f}'.format(round(salary * (percentage / 100), 2))}" for
                        salary, percentage in zip(inflation.salaries, inflation.percent)]
            table_data = zip(inflation.years, inflation.percent, inflation.salaries, inflation.inflated, inflation.inflation_percent)
            return render(request, "calculator/home.html",
                          {"form_a": form_a, "form_b": form_b, "table_data": table_data, "percent": inflation.percent,
                           "country_name": country_name})
    else:
        form_a = UpdateLengthForm()
        form_b = CalcForm()

    return render(request, "calculator/home.html",
                  {"form_a": form_a, "form_b": form_b, "table_data": inflation.table_data, "percent": inflation.percent,
                   "country_name": inflation.country_name})


def update_length(request):
    if request.method == 'POST':
        form_a = UpdateLengthForm(request.POST)
        if form_a.is_valid():
            starting_date = int(form_a.cleaned_data["starting_date"])
            inflation.get_data(starting_date)
            return render(request, "calculator/home.html",
                          {"form_a": form_a, "table_data": inflation.table_data, "percent": inflation.percent,
                           "country_name": inflation.country_name})
        else: # needed for form validation
            return render(request, "calculator/home.html",
                          {"form_a": form_a, "table_data": inflation.table_data, "percent": inflation.percent,
                           "country_name": inflation.country_name})
