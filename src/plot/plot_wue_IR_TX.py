import json, argparse
import src.config as config
import matplotlib.pyplot as plt

# args
ap = argparse.ArgumentParser()
ap.add_argument('--state', type=str, help='State name: Texas, Ireland')
args = ap.parse_args()

state = args.state
files = {
    "meta": "meta_Forth Worth/profile.json" if state == "Texas" else "meta_Clonee/profile.json",
    "azure": "azure_San Antonio/profile.json" if state == "Texas" else "azure_Dublin/profile.json",
    "gcp": "gcp_Midlothian/profile.json" if state == "Texas" else "gcp_Dublin/profile.json",
    "aws": "" if state == "Texas" else "aws_Dublin/profile.json"
}

legend_ncol = 3 #if state == "Texas" else 4

data = dict()
for company, file in files.items():
    if file == "":
        continue
    with open(f"{config.experiments_folder}/{config.d_i}-{config.d_f}/WUE_exp/processed/{file}", "r") as f:

        data[company] = json.load(f)

timestamps = [entry["timestamp"] for entry in data["meta"]["dynamic"]]
static_wue = {company: [data[company]["static"]["WUE"] for timestamp in timestamps] for company in data.keys()}
dynamic_wue = {company: [entry["wue"] for entry in data[company]["dynamic"]] for company in data.keys()}
wet_bulb_temp = {company: [entry["wet_bulb_temp"] for entry in data[company]["dynamic"]] for company in data.keys()}

from src.plot.colors import IBM_color_blind_palette
color = {
    "meta": IBM_color_blind_palette[0], # blue #"#785EF0",# "teal",
    "gcp": IBM_color_blind_palette[1],# purple #"#DC267F",#"dodgerblue",
    "azure": IBM_color_blind_palette[3],# orange #"#FE6100"#"aqua"
    "aws": IBM_color_blind_palette[4] # yellow #"#FFB000"#"limegreen"
}

plt.figure(figsize=(8, 4))

for company in data.keys():
    
    plt.plot(timestamps, static_wue[company], label=f"annual WUE - {company}", color=color[company], linestyle="dashed")
    plt.plot(timestamps, dynamic_wue[company], label=f"hourly WUE - {company}", color=color[company])
    plt.plot(timestamps, wet_bulb_temp[company], label=f"wtb - {files[company].split("/")[0].split("_")[1]}", color=color[company], linestyle="dotted")



#plt.xticks(ticks=timestamps, labels=[ts.split('T')[1][:5] for ts in timestamps], rotation=90)
plt.xticks(ticks=[ts for i,ts in enumerate(timestamps) if i % 12 == 0], labels=[i for i in range(len(timestamps)) if i % 12 == 0])

plt.xlabel('Time', fontsize = config.lable_size)
plt.ylabel('WUE, wet bulb temperature (C°)', fontsize = config.lable_size)
#plt.yscale('log')
plt.legend(ncol=legend_ncol, bbox_to_anchor = (1.01, 1.35))


plt.savefig(f"{config.output_folder}/{config.d_i}-{config.d_f}/WUE_exp/WUE_{state}.pdf",  bbox_inches='tight')
