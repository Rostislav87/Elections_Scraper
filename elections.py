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
# název obce, kód obce, voliči v seznamu, vydané obálky, platné hlasy, kandidující strany


html = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105"
html_doc = requests.get(html)
soup = bs(html_doc.text, "html.parser")

cell = soup.find_all("td")
chart = list()
for elements in cell:
    chart.append(elements.text)
codes = chart[0::3]
towns = chart[1::3]

dict1 = {"codes": codes, "towns": towns}


# Zápis CSV
with open("results_opava.csv", mode="w") as new_csv:
    header = dict1.keys()
    writer = csv.DictWriter(new_csv, dialect="excel-tab", fieldnames=header)
    writer.writeheader()
    

