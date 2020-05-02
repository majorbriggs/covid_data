import functools
import itertools

import requests
from matplotlib import pyplot
from collections import namedtuple

URL_BASE = "https://api.covid19api.com/total/country/"

# mala "klasa" ktora ma pola name i country
Country = namedtuple("Country", ["name", "citizens"])


def confirmed_in_country(country_name: str):
    response = requests.get(URL_BASE + country_name)
    response_json = response.json()
    confirmed = map(lambda day: day["Confirmed"], response_json[:-1])
    return list(confirmed)


def confirmed_per_million(country: Country):  # podalem typ zmiennej
    confirmed = confirmed_in_country(country.name)
    conf_per_mill = []
    for c in confirmed:
        conf_per_mill.append(c / country.citizens)
    return conf_per_mill


def calculate_daily(country_name):
    poland = confirmed_in_country(country_name)
    diff = [j - i for i, j in zip(poland[:-1], poland[1:])]
    return list(diff)

countries = [
    Country("germany", 83.0),
    Country("poland", 38.5),
    Country("italy", 60.4),
    Country("sweden", 10.23),
    Country("belgium", 11.46),
    Country("spain", 46.94),
]

# tworzenie dwoch podwykresow
fig, (countries_plot, daily_plot) = pyplot.subplots(2)
fig.tight_layout(pad=2)  # odstep miedzy subplotami

# rysowanie wykresow dla sumy przypadkow  w krajach
for country in countries:
    countries_plot.plot(confirmed_per_million(country), label=country.name)
countries_plot.set_title("Confirmed cases per million")
countries_plot.legend()

# rysowanie dziennych nowych przypadkow
daily = calculate_daily("germany")
daily_plot.set_title("Daily new cases")
x_axis = list(range(len(daily)))
daily_plot.bar(x_axis, daily, label="Poland")
daily_plot.legend()
pyplot.show()
