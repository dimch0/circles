import os
import requests


GLINK = "https://docs.google.com/spreadsheet/ccc?"
MAIN_KEY = "1X6q2XiXfTcm81bSpwo9Y4WgBPsaVaSBOBcd94qBmpnM"

data_sheets = [
    {
    "filename": './data/scenario_01/data.csv',
    "key":MAIN_KEY,
    "gids":
        {
        "consumable":"571804146",
        "bodies":"1847185351",
        # "doors":"533409778",
        "vendors":"1710936085",
        "qwellen":"1032854683",
        "wear":"628076905",
        "control":"2023181623"
        }
    },
    {
    "filename": './data/scenario_01/gen.csv',
    "key":MAIN_KEY,
    "gids":
        {
        "deck":"2103241586"
        }
    },
    {
    "filename": './res/colors/colors.txt',
    "key":MAIN_KEY,
    "gids":
        {
        "color": "893570609"
        }
    },
]

print "Downloading:"
for dats in data_sheets:
    data = ""
    filename = dats["filename"]
    key = dats["key"]
    gids = dats["gids"]

    for sheet, gid in gids.items():
        print "%s ..." % sheet
        link = "{base}key={key}&gid={gid}&output=csv".format(
            base=GLINK,
            key=key,
            gid=gid)
        response = requests.get(link)
        assert response.status_code == 200, "Wrong status code"
        data += "\n" + response.content

    data = data[1:]

    with open(filename, "wb") as f:
        for line in data:
            f.write(line)
print "Done"