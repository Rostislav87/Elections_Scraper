"""
elections.py: třetí projekt do Engeto Online Python Akademie

author: Rostislav Rabiec
email: rosta.rabiec@icloud.com
discord: Rostislav R.#9305
"""

import requests
from bs4 import BeautifulSoup as bs
import csv

# 1. argument: html = https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105 - okres Opava
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


list_of_voters = list()
list_of_envelopes = list()
list_of_valid_votes = list()
for code in town_codes:   
    town_url = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=14&xobec={code}&xvyber=8105"
    soup2 = bs(requests.get(town_url).text, "html.parser")  
    voters = soup2.find_all("td", {"headers": "sa2"}) # Voliči v seznamu
    for votes in voters:
        list_of_voters.append(votes.text)

    envelopes = soup2.find_all("td", {"headers": "sa3"}) # Vydané obálky
    for envelope in envelopes:
        list_of_envelopes.append(envelope.text)

    valid_votes = soup2.find_all("td", {"headers": "sa6"}) # Platné hlasy
    for votes in valid_votes:
        list_of_valid_votes.append(votes.text)

csv_chart = {
    "Kód obce": town_codes,
    "Název obce": town_names,
    "Voliči v seznamu": list_of_voters,
    "Vydané obálky": list_of_envelopes,
    "Platné hlasy": list_of_valid_votes, 
}



# CSV zápis
# with open("results_opava.csv", mode="w") as new_file:
    # writer = csv.DictWriter(new_file, delimiter="\n")
    



