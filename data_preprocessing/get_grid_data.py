
import os, sys
import csv, json

import utils
import config
import numpy as np
import pandas as pd

STATE_TO_MAP_ZONE = {
    "Iowa": "US-SE-SOCO",
    "Ireland": "IE",
    "Illinois": "DK-DK1",
    "Utah": "US-NW-PACE",
    "North Carolina": "US-CAR-DUK",
    "Texas": "US-TEX-ERCO",
    "Tennessee": "US-TEN-TVA",
    "Virginia": "US-MIDA-PJM",
    "Alabama": "US-TEN-TVA",
    "New Mexico": "US-SW-PNM",
    "Sweden": "SE-SE1",
    "Ohio": "US-MIDA-PJM",
    "Denmark": "DK-DK1",
    "Oregon": "US-NW-PACW",
    "Nebraska": "US-CENT-SWPP",
    "Georgia": "US-SE-SOCO"
}

def get_grid_data():
    """
    Get grid data from the API and save it to a CSV file.
    """
    zones = set()
    dc_names = {}

    for filename in os.listdir("./data_preprocessing/reports"):
        if filename.endswith(".csv"):
            with open(os.path.join("./data_preprocessing/reports", filename), mode='r') as file:
                csv_reader = csv.DictReader(file, delimiter=';')
                for row in csv_reader:
                    state = row["State"] # -> download grid data
                    location = row["Location"]
                    provider = filename.split('.')[0].split("_")[2]
                    dc_names[provider+"_"+location] = STATE_TO_MAP_ZONE[state]

    energy_mix = {}      
    for zone in set(dc_names.values()):
        energy_mix[zone] = utils.get_feature_last24h("power-breakdown", zone)["history"]

    for dc_name, zone in dc_names.items():
        history = energy_mix[zone]
        t_i = history[0]["datetime"]
        t_f = history[-1]["datetime"]
        data_path = f"./data_preprocessing/{t_i}-{t_f}/raw/{dc_name}/energy_mix/"
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        with open("{}/api.json".format(data_path), 'w') as f:
            f.write(json.dumps(history, indent=4))


if __name__ == "__main__":
    get_grid_data()