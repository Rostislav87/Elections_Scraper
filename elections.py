"""
elections.py: třetí projekt do Engeto Online Python Akademie

author: Rostislav Rabiec
email: rosta.rabiec@icloud.com
discord: Rostislav R.#9305
"""

import requests
from bs4 import BeautifulSoup as bs

# 1. argument: html = https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105 # Opava
# 2. arguement: results_opava.csv

html = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105"
html_doc = requests.get(html)
soup = bs(html_doc.text, "html.parser")
cell = soup.find_all("td")
chart = list()
for city in cell:
    chart.append(city.text)

print(chart)
