import src.config as config
import src.models.datacenter as datacenter
import json
import os
data = {}
experiment_data_folder_meta = f"{config.experiments_folder}/{config.d_i}-{config.d_f}/meta_exp/processed/"
experiment_data_folder_cp = f"{config.experiments_folder}/{config.d_i}-{config.d_f}/cp_exp_100MW/processed/"

for dc_name in os.listdir(experiment_data_folder_meta):
    if os.path.isfile(os.path.join(experiment_data_folder_meta, dc_name)): continue
    print(dc_name)
    with open(os.path.join(experiment_data_folder_meta, dc_name)+"/profile.json", 'r') as f:
        data[dc_name] = json.load(f)


for dc_name in os.listdir(experiment_data_folder_cp):
    if os.path.isfile(os.path.join(experiment_data_folder_cp, dc_name)): continue
    print(dc_name)
    with open(os.path.join(experiment_data_folder_cp, dc_name)+"/profile.json", 'r') as f:
        data[dc_name] = json.load(f)
x, wue= [],[]

for dc_name, profile in data.items():

    x.append(dc_name)
    wue.append(profile["static"]['WUE'])

import matplotlib.pyplot as plt
import src.plot.colors as colors
fig, axs = plt.subplots(1, 1, figsize=(10, 5))
axs.bar(x, wue, color=colors.IBM_color_blind_palette[0])
axs.set_xlabel('Data Center')
axs.set_ylabel('WUE')
#axs.set_title('WUE values of Data Centers')
axs.set_xticklabels(x, rotation=45, ha='right')
plt.tight_layout()

plt.savefig(f"{config.output_folder}/{config.d_i}-{config.d_f}/wue_datacenters.pdf")
