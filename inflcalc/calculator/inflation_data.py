import requests
import datetime


class Inflation():
    def __init__(self):
        self.country = "DEU"
        self.start_year = 2016
        response = requests.get(f"https://www.imf.org/external/datamapper/api/v1/PCPIPCH/{self.country}")
        response_country = requests.get(f"https://www.imf.org/external/datamapper/api/v1/countries")
        data_country = response_country.json()
        self.country_name = data_country["countries"][self.country]["label"]
        self.data = response.json()
        self.get_data(self.start_year)


    def get_data(self, start_year):
        today = datetime.date.today()
        year = today.year
        start_year = start_year
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