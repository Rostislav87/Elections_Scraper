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

print("Stahuji data...")
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
data1 = list() # Seznam voličů
data2 = list() # Seznam vydaných obálek
data3 = list() # Seznam platných hlasů
parties = list() # Seznam všech politických strana
party_votes = list() # Seznam všech hlasů za každou obec

for code in town_codes:   
    town_url = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=14&xobec={code}&xvyber=8105"
    soup2 = bs(requests.get(town_url).text, "html.parser")  
  
    voters = soup2.find_all("td", {"headers": "sa2"}) # Voliči v seznamu
    for votes in voters:
        data1.append(votes.text.replace("\xa0", ""))
        
    envelopes = soup2.find_all("td", {"headers": "sa3"}) # Vydané obálky
    for envelope in envelopes:
        data2.append(envelope.text.replace("\xa0", ""))
    
    valid_votes = soup2.find_all("td", {"headers": "sa6"}) # Platné hlasy
    for votes in valid_votes:
        data3.append(votes.text.replace("\xa0", ""))

    parties_tab1 = soup2.find_all("td", {"headers": "t1sa1 t1sb2"}) # Politické strany (1. tabulka)
    parties_tab2 = soup2.find_all("td", {"headers": "t2sa1 t2sb2"}) # Politické strany (2. tabulka)
    parties_votes1 = soup2.find_all("td", {"headers": "t1sa2 t1sb3"}) # Platné hlasy pro každou stranu (1. tabulka)
    parties_votes2 = soup2.find_all("td", {"headers": "t2sa2 t2sb3"}) # Platné hlasy pro každou stranu (2. tabulka)
    parties = [party.text for party in parties_tab1] + [party.text for party in parties_tab2]
    list_of_votes = list()
    for vote in parties_votes1:
        list_of_votes.append(vote.text.replace("\xa0", ""))
    for vote in parties_votes2:
        list_of_votes.append(vote.text.replace("\xa0", ""))
    party_votes.append(list_of_votes)

list_of_votes_sorted_by_parties = [[row[i] for row in party_votes] for i in range(26)]

dict1 = {
    "Kód obce": town_codes,
    "Název obce": town_names,
    "Voliči v seznamu": data1,
    "Vydané obálky": data2,
    "Platné hlasy": data3
    }
dict2 = dict()
for key, item in zip(parties, list_of_votes_sorted_by_parties):
    dict2[key] = item

dict1.update(dict2)

print("Zapisuji data...")
with open("results_opava.csv", mode="w", newline="") as new_file:
    writer = csv.writer(new_file, delimiter=";")    
    writer.writerow(dict1.keys())
    writer.writerows(zip(*dict1.values()))

print("Hotovo.")