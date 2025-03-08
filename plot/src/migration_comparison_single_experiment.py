import argparse, json, os
import matplotlib.pyplot as plt

import config

# args
ap = argparse.ArgumentParser()
ap.add_argument('--algorithm', type=str, help='Algorithm name')
args = ap.parse_args()

# load output data
file_path1 = config.out_path +f"assignments_{args.algorithm}_migration.json"
file_path2 = config.out_path +f"assignments_{args.algorithm}.json"

with open(file_path1, "r") as f:
    assignments_migration = json.load(f)["assignments"]
with open(file_path2, "r") as f:
    assignments_no_migration = json.load(f)["assignments"]


# Extract data for plotting
timestamps = list(assignments_migration.keys())

power_values_migration = [sum([job['power'] for job in assignments_migration[timestamp]])for timestamp in timestamps]
carbon_values_migration = [sum([job['carbon']/10**3  for job in assignments_migration[timestamp]]) for timestamp in timestamps]
water_values_migration = [sum([job['water'] for job in assignments_migration[timestamp]]) for timestamp in timestamps]
land_use_values_migration = [sum([job['land_use']/10**3  for job in assignments_migration[timestamp]]) for timestamp in timestamps]

power_values_no_migration = [sum([job['power'] for job in assignments_no_migration[timestamp]])for timestamp in timestamps]
carbon_values_no_migration = [sum([job['carbon']/10**3  for job in assignments_no_migration[timestamp]]) for timestamp in timestamps]
water_values_no_migration = [sum([job['water'] for job in assignments_no_migration[timestamp]]) for timestamp in timestamps]
land_use_values_no_migration = [sum([job['land_use']/10**3  for job in assignments_no_migration[timestamp]]) for timestamp in timestamps]

# Create subplots with shared x-axis
fig, axs = plt.subplots(3, 1, sharex=True, figsize=(8, 10))
#fig.suptitle(config.names[args.algorithm])

# Plot data
axs[0].plot(timestamps, carbon_values_migration, label="Migration", color=config.colors[args.algorithm])
axs[0].plot(timestamps, carbon_values_no_migration, label="No Migration", color=config.colors[args.algorithm], linestyle='dashed')

axs[1].plot(timestamps, water_values_migration, label="Migration",color=config.colors[args.algorithm])
axs[1].plot(timestamps, water_values_no_migration, label="No Migration", color=config.colors[args.algorithm], linestyle='dashed')

axs[2].plot(timestamps, land_use_values_migration, label="Migration", color=config.colors[args.algorithm])
axs[2].plot(timestamps, land_use_values_no_migration, label="No Migration", color=config.colors[args.algorithm], linestyle='dashed')

# Set labels and titles
#axs[0].set_title("Carbon Emissions")
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
axs[0].legend(ncol=2, bbox_to_anchor = (0.7, 1.15))

plt.tight_layout()

if not os.path.exists(config.plot_path):
    os.makedirs(config.plot_path)
out_path = config.plot_path + f"plot_migration_comparison_{args.algorithm}.png"
plt.savefig(out_path, bbox_inches='tight')