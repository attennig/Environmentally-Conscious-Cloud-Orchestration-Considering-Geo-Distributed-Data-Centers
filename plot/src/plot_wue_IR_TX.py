import json, argparse
import config
import matplotlib.pyplot as plt

# args
ap = argparse.ArgumentParser()
ap.add_argument('--state', type=str, help='State name: Texas, Ireland')
args = ap.parse_args()

state = args.state
files = {
    "meta": "meta_Forth Worth.json" if state == "Texas" else "meta_Clonee.json",
    "azure": "azure_San Antonio.json" if state == "Texas" else "azure_Dublin.json",
    "google": "google_Midlothian.json" if state == "Texas" else "google_Dublin.json"
}

data = dict()
for company, file in files.items():
    with open(config.in_path+file, "r") as f:
        data[company] = json.load(f)

timestamps = [entry["timestamp"] for entry in data["meta"]["dynamic"]]
static_wue = {company: [data[company]["static"]["WUE"] for timestamp in timestamps] for company in data.keys()}
dynamic_wue = {company: [entry["wue"] for entry in data[company]["dynamic"]] for company in data.keys()}
wet_bulb_temp = {company: [entry["wet_bulb_temp"] for entry in data[company]["dynamic"]] for company in data.keys()}

color = {
    "meta": "#785EF0",# "teal",
    "google": "#DC267F",#"dodgerblue",
    "azure": "#FE6100"#"aqua"
}

plt.figure(figsize=(7, 4))

for company in data.keys():
    
    plt.plot(timestamps, static_wue[company], label=f"annual WUE - {company}", color=color[company], linestyle="dashed")
    plt.plot(timestamps, dynamic_wue[company], label=f"hourly WUE - {company}", color=color[company])
    plt.plot(timestamps, wet_bulb_temp[company], label=f"wtb - {files[company].split(".")[0].split("_")[1]}", color=color[company], linestyle="dotted")



plt.xticks(ticks=timestamps, labels=[ts.split('T')[1][:5] for ts in timestamps], rotation=90)
plt.xlabel('Timestamp')
plt.ylabel('WUE, wet bulb temperature (C°)')
#plt.yscale('log')
plt.legend(ncol=3, bbox_to_anchor = (1.01, 1.3))


plt.savefig(f"{config.plot_path}WUE_{state}",  bbox_inches='tight')
