import os
import requests

GLINK = "https://docs.google.com/spreadsheet/ccc?"
data_sheets = [
    {
    "filename":os.path.dirname(__file__) + '/data/scenario_01/data.csv',
    "key":"1X6q2XiXfTcm81bSpwo9Y4WgBPsaVaSBOBcd94qBmpnM",
    "gids":
        {
        "consumable":"571804146",
        "bodies":"1847185351",
        "doors":"533409778",
        "vendors":"1710936085",
        "qwellen":"1032854683",
        "wear":"628076905",
        "crafts":"1972945153",
        "control":"2023181623"
        }
    },
    {
    "filename":os.path.dirname(__file__) + '/data/scenario_01/gen.csv',
    "key":"1X6q2XiXfTcm81bSpwo9Y4WgBPsaVaSBOBcd94qBmpnM",
    "gids":
        {
        "deck":"2103241586"
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