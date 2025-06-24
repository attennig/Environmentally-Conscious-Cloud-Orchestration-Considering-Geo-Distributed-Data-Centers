import argparse, json, os
import matplotlib.pyplot as plt
import src.config as config
from src.plot.utils import get_datapoints


# args
ap = argparse.ArgumentParser()
ap.add_argument('--migration', action='store_true', help='Migration enabled')
ap.add_argument('--algorithms', '--list', nargs='+', help='List of algorithms to plot')
ap.add_argument('--experiment_name', type=str, help='Experiment name')
args = ap.parse_args()



assignments = {}
out_path = f"{config.output_folder}/{config.d_i}-{config.d_f}/{args.experiment_name}"

# load output data
for algo_name in args.algorithms: #config.algorithm.keys():
    assignments[algo_name] = {}
    for seed in config.seeds:
        file_path = f"{out_path}/{seed}_assignments_{algo_name}{'_migration'*args.migration}.json"
        with open(file_path, "r") as f:
            assignments[algo_name][seed] = json.load(f)["assignments"]


# Extract data for plotting
timestamps = list(assignments[algo_name][1].keys())

carbon_mean, water_mean, land_use_mean = {}, {}, {}
carbon_std, water_std, land_use_std = {}, {}, {}

for algo_name in args.algorithms:
    carbon_mean[algo_name], carbon_std[algo_name] = get_datapoints("carbon", assignments[algo_name], timestamps)
    water_mean[algo_name], water_std[algo_name] = get_datapoints("water",assignments[algo_name], timestamps)
    land_use_mean[algo_name], land_use_std[algo_name] = get_datapoints("land_use", assignments[algo_name], timestamps)

"""
power_values = {algo_name: [sum([(job['power']) /len(config.seeds) for job in assignments[algo_name][seed][timestamp]for seed in config.seeds ]) for timestamp in timestamps] for algo_name in args.algorithms}
carbon_values = {algo_name: [sum([(job['carbon']/10**3) /len(config.seeds) for job in assignments[algo_name][seed][timestamp] for seed in config.seeds ]) for timestamp in timestamps] for algo_name in args.algorithms}
water_values = {algo_name: [sum([(job['water']) /len(config.seeds) for job in assignments[algo_name][seed][timestamp] for seed in config.seeds])  for timestamp in timestamps] for algo_name in args.algorithms}
land_use_values = {algo_name: [sum([(job['land_use']/10**3 )/len(config.seeds) for job in assignments[algo_name][seed][timestamp] for seed in config.seeds])  for timestamp in timestamps] for algo_name in args.algorithms}
"""

# subplots with shared x-axis
fig, axs = plt.subplots(3, 1, sharex=True, figsize=(8, 18))

# Plot data
for algo_name in args.algorithms:
    axs[0].errorbar(timestamps, y=carbon_mean[algo_name], yerr=carbon_std[algo_name],label=config.names[algo_name], color=config.colors[algo_name])#, marker=config.marker[algo_name])
    axs[1].errorbar(timestamps, y=water_mean[algo_name], yerr=water_std[algo_name], label=config.names[algo_name], color=config.colors[algo_name])#, marker=config.marker[algo_name])
    axs[2].errorbar(timestamps, y=land_use_mean[algo_name], yerr=land_use_std[algo_name], label=config.names[algo_name], color=config.colors[algo_name])#, marker=config.marker[algo_name])

    """
    axs[0].plot(timestamps, carbon_values[algo_name], label=config.names[algo_name], color=config.colors[algo_name])#, marker=config.marker[algo_name])
    axs[1].plot(timestamps, water_values[algo_name], label=config.names[algo_name], color=config.colors[algo_name])#, marker=config.marker[algo_name])
    axs[2].plot(timestamps, land_use_values[algo_name], label=config.names[algo_name], color=config.colors[algo_name])#, marker=config.marker[algo_name])
    """ 

# Set labels and titles
axs[0].set_ylabel("Carbon footprint (kgCO2)", fontsize = config.lable_size)
axs[1].set_ylabel("Water footprint (l)", fontsize = config.lable_size)
axs[2].set_ylabel("Land footprint (kgCO2)", fontsize = config.lable_size)

# Hide x-axis tick labels for the upper subplots
for ax in axs[:-1]:  # All but the last subplot
    ax.label_outer()

# Set x-axis label on the last subplot
axs[-1].set_xlabel("Time", fontsize = config.lable_size)
#plt.xticks(ticks=timestamps, labels=[ts.split('T')[1][:5] for ts in timestamps], rotation=90)
plt.xticks(ticks=[ts for i,ts in enumerate(timestamps) if i % 12 == 0], labels=[i for i in range(len(timestamps)) if i % 12 == 0])

# Display legend
axs[0].legend(ncol=2, bbox_to_anchor = (1, 1.28))

fig.align_ylabels(axs)

plt.tight_layout()

if not os.path.exists(out_path+"/plot"):
    os.makedirs(out_path+"/plot")
file_path =f"{out_path}/plot/plot_algo_comparison{'_migration'*args.migration}.pdf"
plt.savefig(file_path)