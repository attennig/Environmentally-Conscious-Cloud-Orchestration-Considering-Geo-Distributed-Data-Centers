import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import config

def load_data(file_name):
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"The file {file_name} does not exist.")
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data

def plot_factor_overtime(df, factors, title, xlabel, ylabel, file_name):
    # Plot the data
    plt.figure(figsize=(10, 6))
    for factor in factors:
        plt.plot(df['timestamp'], df[factor], marker='o')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.legend(factors)
    plt.savefig(file_name)

def plot_difference_wue(df, file_name):
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df.wue-df.static_wue, marker='o')
    plt.xlabel("Time")
    plt.ylabel("WUE dyn - WUE")
    plt.title("Comparing declared WUE and estimed WUE")
    plt.grid(True)
    plt.savefig(file_name)
    


def plots(file_name, dc_name):
    data = load_data(file_name)

    # Convert the data to a DataFrame
    df = pd.DataFrame(data["dynamic"])
    import numpy as np
    df["static_wue"] = [data["static"]["WUE"]]*24

    # Convert the timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    import os
    if not os.path.exists(config.plot_path):
        os.makedirs(config.plot_path)

    plot_difference_wue(df,f"{config.plot_path}/WUEdiff_{dc_name}.png")
    """
    plot_factor_overtime(df, ['wue', 'wet_bulb_temp', 'static_wue'], 'WUE and Wet Bulb Temperature over time', 'Time', 'WUE, Wet Bulb Temperature (°C)', 
                        f"{config.plot_path}/WUE_Wet_Bulb_Temperature_{dc_name}.png")
    
    
    plot_factor_overtime(df, ['carbon_intensity'], 'Carbon Intensity over time', 'Time', 'CI (gCO2eq/kWh)',
                        f"{config.plot_path}/Carbon_Intensity_{dc_name}.png")
    plot_factor_overtime(df, ['water_intensity'], 'Water Intensity over time', 'Time', 'EWIF (l/kWh)',
                        f"{config.plot_path}/Water_Intensity_{dc_name}.png")
    plot_factor_overtime(df, ['land_use_intensity'], 'Land Use Intensity over time', 'Time', 'ELIF (m2/kWh)',
                        f"{config.plot_path}/Land_Use_Intensity_{dc_name}.png")
    """


for file in os.listdir(config.in_path):
    if "meta_" in file or "google_" in file or "azure_" in file:
        file_name = config.in_path+file
        dc_name = file.split(".")[0]
        print(dc_name)
        plots(file_name, dc_name)
