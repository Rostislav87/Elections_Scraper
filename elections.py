"""
elections.py: třetí projekt do Engeto Online Python Akademie

author: Rostislav Rabiec
email: rosta.rabiec@icloud.com
discord: Rostislav R.#9305
"""

import requests
from bs4 import BeautifulSoup as bs
import csv

# 1. argument: html = https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105 # Opava
# 2. arguement: results_opava.csv
# Ve výstupu (soubor .csv) každý řádek obsahuje informace pro konkrétní obec. Tedy podobu:
# kód obce, název obce, voliči v seznamu, vydané obálky, platné hlasy, kandidující strany

html = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105" 
soup = bs(requests.get(html).text, "html.parser")
cell = soup.find_all("td")

chart = list()
for elements in cell:
    chart.append(elements.text)
list_codes = chart[0::3] 
list_towns = chart[1::3]
town_codes = list_codes[:-1:]
town_names = list_towns[:-1:]

for code in town_codes:   
    town_url = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=14&xobec={code}&xvyber=8105"
    soup2 = bs(requests.get(town_url).text, "html.parser")  
  






