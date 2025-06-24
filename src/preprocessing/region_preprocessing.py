
import os, sys
import csv, json

import src.utils as utils
import src.config as config
import numpy as np
import pandas as pd

import argparse 

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
    "Georgia": "US-SE-SOCO", 
    "California": "US-CAL-CISO", 
    "Australia": "AU-NSW"
}
intensity_coefficients = {# IPCC https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf median values lifecycle emissions column table A.III.2 page 1335
    "carbon": {
        "nuclear": 12,
        "geothermal": 38,
        "biomass": 740+230/2, # cofirinf + dedicated
        "coal": 820,
        "wind": 11+12/2, # onshore + offshore
        "solar": 27+41+48/3, #Concentrated solar power + PV rooftop + PV utility
        "hydro": 24,
        "gas":490,
        "oil": 720, # SOURCE:https://ourworldindata.org/safest-sources-of-energy
        "unknown": None,
        "hydro discharge": None,
        "battery discharge": None
    }, # gCO2eq/kWh 
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

from src.preprocessing.cclf import loss_factors
def get_CCLF(state: str) -> float:
    """
    Get the Carbon Capture Loss Factor (CCLF) for a given state
    :param state: state name
    :return: CCLF value
    """
    return loss_factors[state]

def _get_intensity(mix: dict, factor: str) -> float:
    intensity = 0 
    for source, power_percentage in mix.items():
        if intensity_coefficients[factor][source] is not None:
            intensity += intensity_coefficients[factor][source] * power_percentage
    return intensity # unit/kWh




def _dynamic_data(city, state, file_path, init_time, final_time):
    wetbulb_temp = utils.wetbulb_temperature_processing(
        city=city, state=state, 
        date_time_start=utils.str_to_date(init_time), date_time_finish=utils.str_to_date(final_time), 
        path=f"{file_path}weather/",
        include="hours"
        )
    
    out_dynamic = []
    history_df = pd.read_csv(f"{file_path}energy_mix/history.csv")

    
    for row in history_df.iterrows():
        timestamp = row[1]["datetime"]
        mix = {
            column: row[1][column]
            for column in row[1].index if column not in ["datetime"]
        }

        total_power = sum(mix.values())
        mix_percentage = {source: power / total_power for source, power in mix.items()} # %
        carbon_intensity = _get_intensity(mix_percentage, "carbon") # gCO2eq/kWh
        water_intensity = _get_intensity(mix_percentage, "water") # l/kWh
        land_use_intensity = _get_intensity(mix_percentage, "land_use") # m2/kWh
        out_dynamic.append({
            "timestamp": timestamp,#date_to_str(timestamp),
            "carbon_intensity": carbon_intensity,       # CI 
            "water_intensity": water_intensity,         # EWIF
            "land_use_intensity": land_use_intensity,    # ELIF
            "wue": utils.wue(cycles_of_concentration, wetbulb_temp[utils.str_to_date(timestamp)]), # WUE
            "wet_bulb_temp": wetbulb_temp[utils.str_to_date(timestamp)]
        })
    return out_dynamic
    

def preprocess(company: str, init_time: str = config.d_i, final_time: str = config.d_f):
    report_name = {
        "meta": "Report_2024_meta.csv",
        "gcp": "Report_2024_gcp.csv",
        "azure": "Report_2022_azure.csv",
        "aws": "Report_x_aws.csv"
    } 
    mean_facility_consuption_avg = 0.876000*10**9 #IEA MIN ESTIMED FOR HYPERSCALE 100MW -> 876000 MWh 1year #0.778*10**9 #META AVG 778833812 kWh

    with open(f"{config.report_folder}/{report_name[company.lower()]}", mode='r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            print(row["Location"])
            city = row["Location"]
            state = row["State"]
            
            wsf = row['water scarcity factor']
            if company == "meta":
                lue = float(row['total space (m^2)']) / (float(row['Facility Electricity Consumption (MWh)'])*10**3 / float(row['PUE'])) # m^2/kWh
                wue_reported_approx = float(row['Water Withdrawal (Ml)'])*10**6  / (float(row['Facility Electricity Consumption (MWh)'])*10**3 / float(row['PUE'])) # l/kWh
            elif company == "gcp":
                IT_consumption_avg = mean_facility_consuption_avg / float(row['PUE'])
                lue = float(row['total space (m^2)']) / IT_consumption_avg # m^2/kWh
                wue_reported_approx = float(row['water withdrawal (l)']) / IT_consumption_avg # l/kWh
            elif company == "azure" or company == "aws":
                IT_consumption_avg = mean_facility_consuption_avg / float(row['PUE'])
                lue = float(row['total space (m^2)']) / IT_consumption_avg # m^2/kWh
                wue_reported_approx = float(row['WUE']) # l/kWh

            out_static = {
                "PUE": row["PUE"], #PUE
                "LUE": lue, #LUE
                "WSF": wsf, #WSF
                "WUE": wue_reported_approx,
                "CCLF": get_CCLF(state)
            }

            dc_name = f"{company}_{city}"

            out_dynamic = _dynamic_data(
                city=city,
                state=state,
                file_path=f"{config.experiments_folder}/{init_time}-{final_time}/raw/{dc_name}/", 
                init_time=init_time,
                final_time=final_time
            )

            out = { 
                "dynamic": out_dynamic,
                "static": out_static
            }
            out_path = f"{config.experiments_folder}/{init_time}-{final_time}/processed/{dc_name}/"
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            with open(f"{out_path}profile.json", 'w') as f:
                json.dump(out, f)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='preprocessing script.')
    parser.add_argument('--init_time', type=str, help='Initial time of simulation')
    parser.add_argument('--final_time', type=str, help='Final time of simulation')
    parser.add_argument('--company', type=str, help='Which company report to preprocess')
    args = parser.parse_args()

    if args.company not in ["meta", "gcp", "azure", "aws"]:
        raise Exception("Company not recognized, please use meta, gcp, azure or aws")

    preprocess(args.company, args.init_time, args.final_time)





"""
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


if args.company == "Google":
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
"""