from django.shortcuts import render, redirect
from .forms import update_length_form, calcForm, set_start_date
from .inflation_data import Inflation

inflation = Inflation()

def landing(request):
    if request.method == "POST":
        form = set_start_date(request.POST)
        if form.is_valid():
            inflation.start_year = int(form.cleaned_data["year"])
            print(inflation.start_year)
            return redirect("index")
    else:
        form = set_start_date()
        return render(request, "calculator/landing.html", {"form": form,})

def index(request):
    inflation.get_data(inflation.start_year)
    years = list(inflation.modified_dict.keys())[::-1]
    percent = [value[2] for value in inflation.modified_dict.values()][::-1]
    inflation_percent = [f"{value[0]}%" for value in inflation.modified_dict.values()][::-1]
    country_name = inflation.country_name
    inflated = [0] * len(years)
    salaries = [0] * len(years)
    if request.method == "POST":
        form = calcForm(request.POST)
        if form.is_valid():
            # extract salaries from post data
            salaries = [float(request.POST.get(f"salaries_{year}")) or 0 for year in years]
            # calculate inflated salaries
            inflated = [round(salary * (percentage / 100), 2) for salary, percentage in zip(salaries, percent)]
            table_data = zip(years, percent, salaries, inflated, inflation_percent)
            return render(request, "calculator/home.html",
                          {"form": form, "table_data": table_data, "percent": percent, "country_name": country_name})
    else:
        form = update_length_form()
    table_data = zip(years, percent, salaries, inflated, inflation_percent)

    return render(request, "calculator/home.html",
                  {"form": form, "table_data": table_data, "percent": percent, "country_name": country_name})

def update_length(request):
    if request.method == 'POST':
        form = update_length_form(request.POST)
        if form.is_valid():
            starting_date = int(form.cleaned_data["starting_date"])
            inflation.get_data(starting_date)
            years = list(inflation.modified_dict.keys())[::-1]
            percent = [value[2] for value in inflation.modified_dict.values()][::-1]
            inflation_percent = [f"{value[0]}%" for value in inflation.modified_dict.values()][::-1]
            country_name = inflation.country_name
            inflated = [0] * len(years)
            salaries = [0] * len(years)
            table_data = zip(years, percent, salaries, inflated, inflation_percent)
            return render(request, "calculator/home.html", {"form": form, "table_data": table_data, "percent": percent, "country_name": country_name})
        else:
            years = list(inflation.modified_dict.keys())[::-1]
            percent = [value[2] for value in inflation.modified_dict.values()][::-1]
            inflation_percent = [f"{value[0]}%" for value in inflation.modified_dict.values()][::-1]
            country_name = inflation.country_name
            inflated = [0] * len(years)
            salaries = [0] * len(years)
            table_data = zip(years, percent, salaries, inflated, inflation_percent)
            return render(request, "calculator/home.html", {"form": form, "table_data": table_data, "percent": percent, "country_name": country_name})

