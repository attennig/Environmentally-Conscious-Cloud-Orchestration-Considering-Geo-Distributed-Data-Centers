import pandas as pd
import json, os

d_i = "2025-05-12T00:00:00.000Z"
d_f = "2025-05-14T23:00:00.000Z"
paths = [
    "data/experiments/2025-05-12T00:00:00.000Z-2025-05-12T23:00:00.000Z",
    "data/experiments/2025-05-13T00:00:00.000Z-2025-05-13T23:00:00.000Z",
    "data/experiments/2025-05-14T00:00:00.000Z-2025-05-14T23:00:00.000Z"
    ]

out_path = f"data/experiments/{d_i}-{d_f}/raw"
os.makedirs(out_path, exist_ok=True)
datacenters = {}
for path in paths:
    for folder in os.listdir(path+"/raw"):
        if folder not in datacenters:
            datacenters[folder] = []

        data = json.load(open(path+"/raw/"+folder+"/energy_mix/api.json", "r"))
        datacenters[folder]+=data
    
for dc, data in datacenters.items():
    
    if not os.path.exists(out_path+"/"+dc):
        os.makedirs(out_path+"/"+dc+"/energy_mix")
    json.dump(data, open(out_path+"/"+dc+"/energy_mix/api.json", "w"), indent=4)
    rows = []
    for entry in data:
        row = entry["powerConsumptionBreakdown"]
        row["datetime"] = entry["datetime"]
        rows.append(row)


    df = pd.DataFrame(rows)
    df.to_csv(out_path+"/"+dc+"/energy_mix/history.csv", index=False)