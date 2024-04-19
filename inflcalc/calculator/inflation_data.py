import requests
import datetime
import pycountry

class Inflation():
    def __init__(self):
        self.country = "DEU"
        self.country_name = "Germany"
        self.start_year = 0
        self.inflated = [0]
        self.salaries = [0]



    def get_data(self, start_year):
        response = requests.get(f"https://www.imf.org/external/datamapper/api/v1/PCPIPCH/{self.country}")
        self.data = response.json()
        today = datetime.date.today()
        year = today.year
        self.start_year = int(start_year)

        self.new_dict = {int(year): value for year, value in
                         self.data["values"]["PCPIPCH"][self.country].items()}  # format the api data

        self.modified_dict = {key: [value, 0, 0] for key, value in
                              self.new_dict.items()}  # make a list out of the values

        self.modified_dict = {key: value for key, value in self.modified_dict.items() if
                              key <= year}  # remove all data after the current year

        self.modified_dict = {key: value for key, value in self.modified_dict.items() if
                              key >= start_year}  # remove all data before the start year

        for year in range(start_year, year + 1):  # calculate the inflation percentage starting from the start year
            remaining_percentage = 100
            for key, value in self.modified_dict.items():
                if key <= year:
                    remaining_percentage *= round((100 - value[0]) / 100, 2)
            self.modified_dict[year][2] = round(remaining_percentage, 2)

        self.years = list(self.modified_dict.keys())[::-1]
        self.percent = [value[2] for value in self.modified_dict.values()][::-1]
        self.inflation_percent = [f"{value[0]}%" for value in self.modified_dict.values()][::-1]

        if self.inflated[0] is not 0:
            dif = len(self.years) - len(self.inflated)
            for i in range(dif):
                self.inflated.append(0)
                self.salaries.append(0)
        else:
            self.inflated = [0] * len(self.years)
            self.salaries = [0] * len(self.years)
        self.table_data = zip(self.years, self.percent, self.salaries, self.inflated,
                         self.inflation_percent)