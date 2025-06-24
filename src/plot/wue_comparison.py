import src.config as config
import json
import os
data = {}
experiment_data_folder_meta = f"{config.experiments_folder}/{config.d_i}-{config.d_f}/meta_exp/processed/"
experiment_data_folder_cp = f"{config.experiments_folder}/{config.d_i}-{config.d_f}/cp_exp_100MW/processed/"

for dc_name in os.listdir(experiment_data_folder_meta):
    if os.path.isfile(os.path.join(experiment_data_folder_meta, dc_name)): continue
    with open(os.path.join(experiment_data_folder_meta, dc_name)+"/profile.json", 'r') as f:
        data[dc_name] = json.load(f)


for dc_name in os.listdir(experiment_data_folder_cp):
    if os.path.isfile(os.path.join(experiment_data_folder_cp, dc_name)): continue
    with open(os.path.join(experiment_data_folder_cp, dc_name)+"/profile.json", 'r') as f:
        data[dc_name] = json.load(f)

import src.plot.colors as colors
from matplotlib.patches import Patch

x, wue, c, h = [], [], [], []
sorted_data = {key: value for key, value in sorted(data.items(), reverse=True)}
for dc_name, profile in sorted_data.items():

    x.append(dc_name)
    wue.append(profile["static"]['WUE'])
    if dc_name.split("_")[0] == "meta":
        c.append(colors.IBM_color_blind_palette[0])
        h.append('')
    else:
        c.append(colors.IBM_color_blind_palette[2])
        if dc_name.split("_")[0] == "gcp":
            h.append('..')
        elif dc_name.split("_")[0] == "azure":
            h.append('oo')
        else:
            h.append('OO')
legend_elements = [
    Patch(facecolor=colors.IBM_color_blind_palette[0], label='Scenario 1 (Meta)'), 
    Patch(facecolor=colors.IBM_color_blind_palette[2], label='Scenario 2 (Cloud Providers)')
    ]

import numpy as np


text_s1 = f"min:{np.min(wue[:13]):.3f}\nmax:{np.max(wue[:13]):.3f}\nmean:{np.mean(wue[:13]):.3f}\nstd:{np.std(wue[:13]):.3f}\nvar:{np.var(wue[:13]):.3f}"
text_s2 = f"min:{np.min(wue[13:]):.3f}\nmax:{np.max(wue[13:]):.3f}\nmean:{np.mean(wue[13:]):.3f}\nstd:{np.std(wue[13:]):.3f}\nvar:{np.var(wue[13:]):.3f}"
import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 1, figsize=(10, 5))
axs.bar(x, wue, color=c, hatch=h )
axs.set_xlabel('Data Center')
axs.set_ylabel('WUE')
#axs.set_title('WUE values of Data Centers')
axs.set_xticklabels(x, rotation=45, ha='right')
axs.legend(handles=legend_elements, loc='upper center')
plt.text(0.02, 0.85, text_s1, transform=axs.transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.5))
plt.text(0.89, 0.85, text_s2, transform=axs.transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.5))
plt.tight_layout()
plt.savefig(f"{config.output_folder}/{config.d_i}-{config.d_f}/wue_datacenters.pdf")

