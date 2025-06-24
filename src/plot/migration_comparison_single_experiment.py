import argparse, json, os
import matplotlib.pyplot as plt
import src.config as config
from src.plot.utils import get_datapoints

ap = argparse.ArgumentParser()
ap.add_argument('--algorithm', type=str, help='Algorithm name')
ap.add_argument('--experiment_name', type=str, help='Experiment name')

args = ap.parse_args()

out_path = f"{config.output_folder}/{config.d_i}-{config.d_f}/{args.experiment_name}"
# load output data

assignments_migration = {}
assignments_no_migration = {}

for seed in config.seeds:
    with open(f"{out_path}/{seed}_assignments_{args.algorithm}_migration.json", "r") as f:
        assignments_migration[seed] = json.load(f)["assignments"]
    with open(f"{out_path}/{seed}_assignments_{args.algorithm}.json", "r") as f:
        assignments_no_migration[seed] = json.load(f)["assignments"]


# Extract data for plotting
timestamps = assignments_migration[1].keys()



carbon_mean, carbon_std = get_datapoints("carbon", assignments_migration, timestamps)
water_mean, water_std = get_datapoints("water",assignments_migration, timestamps)
land_use_mean, land_use_std = get_datapoints("land_use", assignments_migration, timestamps)
no_carbon_mean, no_carbon_std = get_datapoints("carbon", assignments_no_migration, timestamps)
no_water_mean, no_water_std = get_datapoints("water",assignments_no_migration, timestamps)
no_land_use_mean, no_land_use_std = get_datapoints("land_use", assignments_no_migration, timestamps)

"""
power_values_migration = [sum([(job['power']) /len(config.seeds) for seed in config.seeds for job in assignments_migration[seed][timestamp] ]) for timestamp in timestamps]
carbon_values_migration = [sum([(job['carbon']/10**3) /len(config.seeds)  for job in assignments_migration[seed][timestamp] for seed in config.seeds]) for timestamp in timestamps]
water_values_migration = [sum([(job['water']) /len(config.seeds) for job in assignments_migration[seed][timestamp] for seed in config.seeds]) for timestamp in timestamps]
land_use_values_migration = [sum([(job['land_use']/10**3) /len(config.seeds)  for job in assignments_migration[seed][timestamp] for seed in config.seeds]) for timestamp in timestamps]

power_values_no_migration = [sum([(job['power']) /len(config.seeds) for job in assignments_no_migration[seed][timestamp] for seed in config.seeds])for timestamp in timestamps]
carbon_values_no_migration = [sum([(job['carbon']/10**3) /len(config.seeds)  for job in assignments_no_migration[seed][timestamp] for seed in config.seeds]) for timestamp in timestamps]
water_values_no_migration = [sum([(job['water']) /len(config.seeds) for job in assignments_no_migration[seed][timestamp] for seed in config.seeds]) for timestamp in timestamps]
land_use_values_no_migration = [sum([(job['land_use']/10**3 ) /len(config.seeds) for job in assignments_no_migration[seed][timestamp] for seed in config.seeds]) for timestamp in timestamps]


# Create subplots with shared x-axis
fig, axs = plt.subplots(3, 1, sharex=True, figsize=(6, 4))
#fig.suptitle(config.names[args.algorithm])

# Plot data
axs[0].plot(timestamps, carbon_values_migration, label="Migration", color=config.colors[args.algorithm])#, marker=config.marker[args.algorithm])
axs[0].plot(timestamps, carbon_values_no_migration, label="No Migration",linestyle='dashed', color=config.colors[args.algorithm])#, marker=config.marker[args.algorithm])

axs[1].plot(timestamps, water_values_migration, label="Migration",color=config.colors[args.algorithm])#, marker=config.marker[args.algorithm])
axs[1].plot(timestamps, water_values_no_migration, label="No Migration", linestyle='dashed', color=config.colors[args.algorithm])#, marker=config.marker[args.algorithm])

axs[2].plot(timestamps, land_use_values_migration, label="Migration", color=config.colors[args.algorithm])#, marker=config.marker[args.algorithm])
axs[2].plot(timestamps, land_use_values_no_migration, label="No Migration", linestyle='dashed', color=config.colors[args.algorithm])#, marker=config.marker[args.algorithm])
"""


fig, axs = plt.subplots(3, 1, sharex=True, figsize=(10, 5))

axs[0].errorbar(x=timestamps, y=no_carbon_mean, yerr=no_carbon_std, 
                linewidth=1.5,
                capsize=5,
                elinewidth=1,
                linestyle='--',
                label="No Migration",color=config.colors_shadow[args.algorithm])#, marker=config.marker[algorithm])
axs[1].errorbar(x=timestamps, y=no_water_mean, yerr=no_water_std,
                linewidth=1.5,
                capsize=5,
                elinewidth=1,
                linestyle='--',
                label="No Migration", color=config.colors_shadow[args.algorithm])#, marker=config.marker[algorithm])
axs[2].errorbar(x=timestamps, y=no_land_use_mean, yerr=no_land_use_std,
                linewidth=1.5,
                capsize=5,
                elinewidth=1,
                linestyle='--',
                label="No Migration", color=config.colors_shadow[args.algorithm])#, marker=config.marker[algorithm])

axs[0].errorbar(x=timestamps, y=carbon_mean, yerr=carbon_std,
                linewidth=1,
                capsize=3,
                elinewidth=0.5,
                label="Migration", color=config.colors[args.algorithm])#, marker=config.marker[algorithm])

axs[1].errorbar(x=timestamps, y=water_mean, yerr=no_water_std, 
                linewidth=1,
                capsize=3,
                elinewidth=0.5,
                label="Migration",color=config.colors[args.algorithm])#, marker=config.marker[algorithm])

axs[2].errorbar(x=timestamps, y=land_use_mean, yerr=land_use_std, 
                linewidth=1,
                capsize=3,
                elinewidth=0.5,
                label="Migration", color=config.colors[args.algorithm])#, marker=config.marker[algorithm])


# Set labels and titles
#axs[0].set_title("Carbon Emissions")
axs[0].set_ylabel("Carbon \nfootprint (kgCO2)", fontsize = config.lable_size)
axs[1].set_ylabel("Water \nfootprint (l)", fontsize = config.lable_size)
axs[2].set_ylabel("Land \nfootprint (kgCO2)", fontsize = config.lable_size)

# Hide x-axis tick labels for the upper subplots
for ax in axs[:-1]:  # All but the last subplot
    ax.label_outer()

# Set x-axis label on the last subplot
axs[-1].set_xlabel("Time", fontsize = config.lable_size)
#plt.xticks(ticks=timestamps, labels=[ts.split('T')[1][:5] for ts in timestamps], rotation=90)
plt.xticks(ticks=[ts for i,ts in enumerate(timestamps) if i % 12 == 0], labels=[i for i in range(len(timestamps)) if i % 12 == 0])


# Display legend

axs[0].legend(ncol=2, bbox_to_anchor = (0.65, 1.35))

plt.tight_layout()
fig.align_ylabels(axs)

if not os.path.exists(f"{out_path}/plot"):
    os.makedirs(f"{out_path}/plot")
out_path = f"{out_path}/plot/plot_migration_comparison_{args.algorithm}.pdf"
plt.savefig(out_path, bbox_inches='tight')

