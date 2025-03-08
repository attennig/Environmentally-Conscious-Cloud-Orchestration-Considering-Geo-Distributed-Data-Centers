import argparse, json, os
import matplotlib.pyplot as plt

import config



# args
ap = argparse.ArgumentParser()
ap.add_argument('--migration', action='store_true', help='Migration enabled')
args = ap.parse_args()


assignments = {}

# load output data
for algo_name in config.algorithm.keys():
    file_path = config.out_path +f"assignments_{algo_name}{'_migration'*args.migration}.json"
    with open(file_path, "r") as f:
        assignments[algo_name] = json.load(f)["assignments"]

# Extract data for plotting
timestamps = list(assignments[algo_name].keys())
power_values = {algo_name: [sum([job['power'] for job in assignments[algo_name][timestamp]])for timestamp in timestamps] for algo_name in config.algorithm.keys()}
carbon_values = {algo_name: [sum([job['carbon']/10**3  for job in assignments[algo_name][timestamp]]) for timestamp in timestamps] for algo_name in config.algorithm.keys()}
water_values = {algo_name: [sum([job['water'] for job in assignments[algo_name][timestamp]]) for timestamp in timestamps] for algo_name in config.algorithm.keys()}
land_use_values = {algo_name: [sum([job['land_use']/10**3  for job in assignments[algo_name][timestamp]]) for timestamp in timestamps] for algo_name in config.algorithm.keys()}

# subplots with shared x-axis
fig, axs = plt.subplots(3, 1, sharex=True, figsize=(8, 10))

# Plot data
for algo_name in config.algorithm.keys():
    axs[0].plot(timestamps, carbon_values[algo_name], label=config.names[algo_name], color=config.colors[algo_name])
    axs[1].plot(timestamps, water_values[algo_name], label=config.names[algo_name], color=config.colors[algo_name])
    axs[2].plot(timestamps, land_use_values[algo_name], label=config.names[algo_name], color=config.colors[algo_name])


# Set labels and titles
axs[0].set_ylabel("Carbon footprint (kgCO2)")
axs[1].set_ylabel("Water footprint (l)")
axs[2].set_ylabel("Land footprint (kgCO2)")

# Hide x-axis tick labels for the upper subplots
for ax in axs[:-1]:  # All but the last subplot
    ax.label_outer()

# Set x-axis label on the last subplot
axs[-1].set_xlabel("Time")
plt.xticks(ticks=timestamps, labels=[ts.split('T')[1][:5] for ts in timestamps], rotation=90)

# Display legend
axs[0].legend(ncol=2, bbox_to_anchor = (0.85, 1.25))


plt.tight_layout()

if not os.path.exists(config.plot_path):
    os.makedirs(config.plot_path)

file_path = config.plot_path + f"plot_algo_comparison{'_migration'*args.migration}.png"
plt.savefig(file_path)