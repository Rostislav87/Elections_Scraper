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


def main():
    check_arguments()
    make_soup()
    get_all_results()
    create_csv()

def check_arguments():
    if len(sys.argv) != 3:
        return print("Zadej skript, odkaz a csv soubor pro spuštění programu."), sys.exit()
    elif "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105" not in sys.argv[1]:
        return print("Zadal jsi špatný odkaz."), sys.exit()
    elif ".csv" not in sys.argv[2]:
        return print("Výstupní soubor musí být ve formátu .csv"), sys.exit()
    else:
        return print(f"Spouštím skript {sys.argv[0]}\nStahuji data z {sys.argv[1]}")
    

def make_soup():
    soup = bs(requests.get(sys.argv[1]).text, "html.parser")
    return soup.find_all("td")

def get_all_results():
    chart = list()
    for elements in make_soup():
        chart.append(elements.text)
    list_codes = chart[0::3] 
    list_towns = chart[1::3]

    town_codes = list_codes[:-1:] # Seznam kódů obcí
    town_names = list_towns[:-1:] # Seznam názvů obcí
    list_voters = list() # Seznam voličů
    list_envelopes = list() # Seznam vydaných obálek
    list_valid_votes = list() # Seznam platných hlasů
    parties = list() # Seznam všech politických strana
    party_votes = list() # Seznam všech hlasů za každou obec

    for code in town_codes:   
        town_url = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=14&xobec={code}&xvyber=8105"
        soup2 = bs(requests.get(town_url).text, "html.parser")  
    
        voters = soup2.find_all("td", {"headers": "sa2"}) # Voliči v seznamu
        for votes in voters:
            list_voters.append(votes.text.replace("\xa0", ""))
            
        envelopes = soup2.find_all("td", {"headers": "sa3"}) # Vydané obálky
        for envelope in envelopes:
            list_envelopes.append(envelope.text.replace("\xa0", ""))
        
        valid_votes = soup2.find_all("td", {"headers": "sa6"}) # Platné hlasy
        for votes in valid_votes:
            list_valid_votes.append(votes.text.replace("\xa0", ""))

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
        "Voliči v seznamu": list_voters,
        "Vydané obálky": list_envelopes,
        "Platné hlasy": list_valid_votes
        }
    dict2 = dict()
    for key, item in zip(parties, list_of_votes_sorted_by_parties):
        dict2[key] = item

    dict1.update(dict2)
    return dict1


def create_csv():
    print("Zapisuji data...")
    file = sys.argv[2] # výstupní soubor.csv 
    with open(file, mode="w", newline="", encoding="utf-8") as new_file:
        writer = csv.writer(new_file, delimiter=";")    
        writer.writerow(get_all_results().keys())
        writer.writerows(zip(*get_all_results().values()))
    print(f"Hotovo. Soubor {sys.argv[2]} byl vytvořen.")


if __name__ == "__main__":
    main()