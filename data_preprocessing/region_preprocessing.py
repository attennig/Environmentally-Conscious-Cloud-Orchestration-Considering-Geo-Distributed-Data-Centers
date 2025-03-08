import argparse
from utils import str_to_date, date_to_str, wetbulb_temperature_processing, wue
import json, os

cycles_of_concentration = 10

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
intensity_coefficients = {
    "carbon": {
        "nuclear": 6,
        "geothermal": None,
        "biomass": 154,
        "coal": 970,
        "wind": 11,
        "solar": 53,
        "hydro": 24,
        "gas": 440,
        "oil": 720,
        "unknown": None,
        "hydro discharge": None,
        "battery discharge": None
    }, # gCO2eq/kWh SOURCE:https://ourworldindata.org/safest-sources-of-energy
    "water": {
        "nuclear": 1.788,
        "geothermal": 9.741,
        "biomass": 1.892,
        "coal": 2.089,
        "wind": 0.0015,
        "solar": 2.001,
        "hydro": 36.765,
        "gas": 2.214,
        "oil": None,
        "unknown": None,
        "hydro discharge": None,
        "battery discharge": None
    }, # l/kWh SOURCE: 
    "land_use": {
        "nuclear": 0.0003,
        "geothermal": None,
        "biomass": None,
        "coal": 0.021,
        "wind": 0.1242,
        "solar": 0.022,
        "hydro": 0.033,
        "gas": 0.0013,
        "oil": None,
        "unknown": None,
        "hydro discharge": None,
        "battery discharge": None
    } # m2/kWh  SOURCE: https://ourworldindata.org/land-use-per-energy-source
}

def _get_intensity(mix: dict, factor: str) -> float:
    intensity = 0 
    for source, power_percentage in mix.items():
        if intensity_coefficients[factor][source] is not None:
            intensity += intensity_coefficients[factor][source] * power_percentage
    return intensity # unit/kWh

def _dynamic_data(city, file_path):
    with open(file_path, 'r') as f:
        history = json.load(f)["history"]

    wetbulb_temp = wetbulb_temperature_processing(city=city, date_time_start=str_to_date(args.init_time), date_time_finish=str_to_date(args.final_time), include="hours")
    
    out_dynamic = []
    for row_h in history:
        timestamp = str_to_date(row_h["datetime"])
        mix = row_h["powerConsumptionBreakdown"]
        total_power = sum(mix.values())
        mix_percentage = {source: power / total_power for source, power in mix.items()} # %
        carbon_intensity = _get_intensity(mix_percentage, "carbon") # gCO2eq/kWh
        water_intensity = _get_intensity(mix_percentage, "water") # l/kWh
        land_use_intensity = _get_intensity(mix_percentage, "land_use") # m2/kWh
        out_dynamic.append({
            "timestamp": date_to_str(timestamp),
            "carbon_intensity": carbon_intensity,       # CI 
            "water_intensity": water_intensity,         # EWIF
            "land_use_intensity": land_use_intensity,    # ELIF
            "wue": wue(cycles_of_concentration, wetbulb_temp[timestamp]), # WUE
            "wet_bulb_temp": wetbulb_temp[timestamp]
        })
    return out_dynamic
    

parser = argparse.ArgumentParser(description='preprocessing script.')
parser.add_argument('--init_time', type=str, help='Initial time of simulation')
parser.add_argument('--final_time', type=str, help='Final time of simulation')
parser.add_argument('--company', type=str, help='Which company report to preprocess')
args = parser.parse_args()

path = f"./data_preprocessing/{args.init_time}-{args.final_time}/"

mean_facility_consuption_avg = 0.778*10**9 #META AVG 778833812 kWh
import csv

if args.company == "Meta":
    with open('./data_preprocessing/Report_2024_Meta.csv', mode='r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            print(row["Location"])
            city = row["Location"]
            state = row["State"]
            lue = float(row['total space (m^2)']) / (float(row['Facility Electricity Consumption (MWh)'])*10**3 / float(row['PUE'])) # m^2/kWh
            wsf = row['water scarcity factor']
            wue_reported_approx = float(row['Water Withdrawal (Ml)'])*10**6  / (float(row['Facility Electricity Consumption (MWh)'])*10**3 / float(row['PUE'])) # l/kWh

            out_static = {
                "PUE": row["PUE"], #PUE
                "LUE": lue, #LUE
                "WSF": wsf, #WSF
                "WUE": wue_reported_approx
            }

            out_dynamic = _dynamic_data(
                city=city,
                file_path=f"{path}energy_mix_{STATE_TO_MAP_ZONE[state]}.json"
            )

            out = { 
                "dynamic": out_dynamic,
                "static": out_static
            }
            out_path = f"./data/{args.init_time}-{args.final_time}/"
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            with open(f"{out_path}meta_{city}.json", 'w') as f:
                json.dump(out, f)


if  args.company == "Google":
    with open('./data_preprocessing/Report_2024_Google.csv', mode='r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            print(row["Location"])
            city = row["Location"]
            state = row["State"]
            IT_consumption_avg = mean_facility_consuption_avg / float(row['PUE'])
            lue = float(row['total space (m^2)']) / IT_consumption_avg # m^2/kWh
            wsf = row['water scarcity factor']
            wue_reported_approx = float(row['water withdrawal (l)']) / IT_consumption_avg # l/kWh
            out_static = {
                "PUE": row["PUE"], #PUE
                "LUE": lue, #LUE
                "WSF": wsf, #WSF
                "WUE": wue_reported_approx,
            }

            out_dynamic = _dynamic_data(
                city=city,
                file_path=f"{path}energy_mix_{STATE_TO_MAP_ZONE[state]}.json"
            )
            
            out = { 
                "dynamic": out_dynamic,
                "static": out_static
            }
            out_path = f"./data/{args.init_time}-{args.final_time}/"
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            with open(f"{out_path}google_{city}.json", 'w') as f:
                json.dump(out, f)


if  args.company == "Azure":
    with open('./data_preprocessing/Report_2022_Azure.csv', mode='r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            print(row["Location"])
            city = row["Location"]
            state = row["State"]
            IT_consumption_avg = mean_facility_consuption_avg / float(row['PUE'])
            lue = float(row['total space (m^2)']) / IT_consumption_avg # m^2/kWh
            wsf = row['water scarcity factor']
            wue_reported_approx = float(row['WUE'])

            out_static = {
                "PUE": row["PUE"], #PUE
                "LUE": lue, #LUE
                "WSF": wsf, #WSF
                "WUE": wue_reported_approx
            }

            out_dynamic = _dynamic_data(
                city=city,
                file_path=f"{path}energy_mix_{STATE_TO_MAP_ZONE[state]}.json"
            )
            
            out = { 
                "dynamic": out_dynamic,
                "static": out_static
            }
            out_path = f"./data/{args.init_time}-{args.final_time}/"
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            with open(f"{out_path}azure_{city}.json", 'w') as f:
                json.dump(out, f)
