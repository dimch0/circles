import requests

GLINK = "https://docs.google.com/spreadsheet/ccc?"
data_sheets = [
    {
    "filename" : "../data/scenario_01/scenario_01.csv",
    "key"      : "1X6q2XiXfTcm81bSpwo9Y4WgBPsaVaSBOBcd94qBmpnM",
    "gids"     :
        {
        "gid_consumable" : "571804146",
        "gid_bodies"     : "1847185351",
        "gid_doors"      : "533409778",
        "gid_vendors"    : "1710936085",
        "gid_quellen"    : "1032854683",
        "gid_wear"       : "628076905",
        "gid_crafts"     : "1972945153",
        "control"        : "2023181623"
        }
    },
]

for dats in data_sheets:
    print "Downloading"
    data = ""
    filename = dats["filename"]
    key = dats["key"]
    gids = dats["gids"]

    for sheet, gid in gids.items():
        print "..."
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