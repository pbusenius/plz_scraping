import sys
import json
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


bundeslaender = ["baden-wuerttemberg", "bayern", "berlin", "brandenburg", "bremen", "hamburg", "hessen",
                 "mecklenburg-vorpommern", "niedersachsen", "nordrhein-westfalen", "rheinland-pfalz", "saarland",
                 "sachsen", "sachsen-anhalt", "schleswig-holstein", "thueringen"]


def get_plz_data():
    data = []
    agent = {"User-Agent": "Mozilla/5.0"}

    for i in tqdm(range(len(bundeslaender))):
        url = f"https://home.meinestadt.de/{bundeslaender[i]}/postleitzahlen"

        p = requests.get(url, headers=agent)

        soup = BeautifulSoup(p.content, "html.parser")

        table_body = soup.find('tbody')
        rows = table_body.find_all('tr', {"class": "m-table__row"})

        for row in rows:
            columns = row.find_all("td", {"class": "m-table__data"})
            if columns[0]["data-label"] == "PLZ":

                plz_list = columns[0].find_all("p", {"class": "m-textLink__link"})

                for plz in plz_list:
                    data_point = dict(plz=plz.text.strip(),
                                      stadt=columns[1].text.strip(),
                                      stadtteil=columns[2].text.strip(),
                                      landkreis=columns[3].text.strip(),
                                      bundesland=columns[4].text.strip())

                    data.append(data_point)

    return data


def json_export(plz_data):
    with open("plz_db.json", "w", encoding="utf-8") as file:
        json.dump(dict(plz=plz_data), file, indent=4, sort_keys=True, ensure_ascii=False)


def csv_export(plz_data):
    with open("plz_db.csv", "w", encoding="UTF-8") as file:
        line = "PLZ;Stadt;Stadtteil;Landkreis;Bundesland\n"
        file.write(line)
        for p in plz_data:
            plz = p["plz"]
            stadt = p["stadt"]
            stadtteil = p["stadtteil"]
            landkreis = p["landkreis"]
            bundesland = p["bundesland"]

            line = f"{plz};{stadt};{stadtteil};{landkreis};{bundesland}\n"

            file.write(line)
    pass


def sqlite_export(plz_data):
    # TODO: implement sqlite export
    pass


plz_db = get_plz_data()

command = ""
if len(sys.argv) > 1:
    command = sys.argv[1]

if command == "--json" or command == "-j":
    json_export(plz_db)
elif command == "--csv" or command == "-c":
    csv_export(plz_db)
elif command == "--sqlite" or command == "-s":
    sqlite_export(plz_db)


