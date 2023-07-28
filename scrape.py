from time import sleep
import requests
import bs4
import json
import sqlite3


# GRAB INITIAL CAR SEARCH RESULTS
# https://www.hendrickcars.com/all-inventory/index.htm?geoZip=28209&geoRadius=50

base_url = "https://www.hendrickcars.com"

url_path = (
    "/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getInventory"
)

url_start_param = 0

url_params = {"geoZip": 28209, "geoRadius": 50, "start": url_start_param}

url_hdrs = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# CONNECT TO SQLITE DB AND STORE
db = sqlite3.connect(database="cars.db")

# PRIMARY CODE IN A FUNCTION
def add_to_db():
    global url_start_param
    res = requests.get(
        url=f"{base_url}{url_path}", params=url_params, headers=url_hdrs
    )

    # res.status_code  # 200 MEANS SUCCESS

    # res.content  # EVERYTHING FROM THE WEBPAGE

    j = res.json()  # Returns JSON

    # DUMPING JSON AS A STRING TO A FILE
    # with open('results.json', 'w') as f:
    #     f.write(json.dumps(j))

    sql_insert_template = "INSERT INTO inventory (accountId, askingPrice, autodataCaId, bodyStyle, chromeId, classification, driveLine, engine, engineSize, exteriorColor, fuelType, interiorColor, internetPrice, inventoryDate, inventoryType, link, make, model, modelCode, msrp, newOrUsed, status, stockNumber, transmission, trim, uuid, vin, certified, modelYear, dealerName, dealerCity, dealerState) VALUES {};"

    all_values = []

    def add_key_if_exists(k: str, d: dict):
        if k in d.keys():
            #return d[k]
            return d[k].__str__().replace("'","''")
        else:
            return ""

    fields = [
        "accountId",
        "askingPrice",
        "autodataCaId",
        "bodyStyle",
        "chromeId",
        "classification",
        "driveLine",
        "engine",
        "engineSize",
        "exteriorColor",
        "fuelType",
        "interiorColor",
        "internetPrice",
        "inventoryDate",
        "inventoryType",
        "link",
        "make",
        "model",
        "modelCode",
        "msrp",
        "newOrUsed",
        "status",
        "stockNumber",
        "transmission",
        "trim",
        "uuid",
        "vin",
        "certified",
        "modelYear",
    ]

    for x in range(len(j["pageInfo"]["trackingData"])):
        c = j["pageInfo"]["trackingData"][x]
        record = []
        for r in fields:
            record.append(add_key_if_exists(r, c))

        record.append(c["address"]["accountName"])
        record.append(c["address"]["city"])
        record.append(c["address"]["state"])
        all_values.append(
            "(" + ", ".join(["'" + x.__str__() + "'" for x in record]) + ")"
        )

    all_values_f = ", ".join(all_values)

    sql_insert = sql_insert_template.format(all_values_f)

    db.execute(sql_insert)

    db.commit()

    url_params['start'] += 18

    sleep(1)

    # START PAGINATION FUNCTION HERE
for i in range(252):
    print(f"#{i}")
    add_to_db()


