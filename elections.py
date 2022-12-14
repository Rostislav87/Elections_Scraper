"""
elections.py: třetí projekt do Engeto Online Python Akademie

author: Rostislav Rabiec
email: rosta.rabiec@icloud.com
discord: Rostislav R.#9305
"""

import sys
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

town_codes = list_codes[:-1:] # Seznam kódů obcí
town_names = list_towns[:-1:] # Seznam názvů obcí
list_of_voters = list() # Seznam voličů 
list_of_envelopes = list() # Seznam vydaných obálek
list_of_valid_votes = list() # Seznam platných hlasů

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


    parties_votes1 = soup2.find_all("td", {"headers": "t1sa2 t1sb3"}) # Platné hlasy pro kažou pol. stranu 1
    parties_votes2 = soup2.find_all("td", {"headers": "t2sa2 t2sb3"}) # Platné hlasy pro kažou pol. stranu 2
    
       

# CSV zápis
parties_url = "https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=14"
soup3 = bs(requests.get(parties_url).text, "html.parser")
parties1 = soup3.find_all("td", {"headers": "t1sa1 t1sb2"}) # Politické strany 1 
parties2 = soup3.find_all("td", {"headers": "t2sa1 t2sb2"}) # Politické strany 2

header = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
for party in parties1:
    header.append(party.text)
for party in parties2:
    header.append(party.text)

rows = zip(town_codes, town_names, list_of_voters, list_of_envelopes, list_of_valid_votes)

# with open("results_opava.csv", mode="w", newline="") as new_file:
#     writer = csv.writer(new_file, delimiter=";") 
#     writer.writerow(header)
#     for row in rows:
#         writer.writerow(row)



