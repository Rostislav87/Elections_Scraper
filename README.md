# Elections Scraper - projekt č. 3

Program Elections Scraper je skript, který stahuje volební výsledky do poslanecké sněmovny za rok 2017 a výsledky zapíše do tabulky ve formátu CSV.
Zdrojem je webová stránka https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ, odkaz Moravskoslezský kraj, okres Opava.
Program byl vytvořen v prostředí Visual Studio Code za pomocí dvou knihoven třetích stran viz. soubor requirements.txt, který obsahuje název a verzi každé knihovny. Knihovny byly nainstalovány prostřednictvím zabudovaného terminálu VS Code pomocí příkazu pip install "název knihovny" např. pip install requests.
Program se spouští v terminálu zadáním třech argumentů: 1. název skriptu ve formátu .py, 2. přesně zadanou webovou stránku, která obsahuje volební výsledky za okres Opava, 3. název výstupního souboru, do kterého se výsledky budou zapisovat. Soubor musí být ve formátu CSV např. results_opava.csv.






