import argparse, json, os
import matplotlib.pyplot as plt

import config

# args
ap = argparse.ArgumentParser()
ap.add_argument('--algorithm', type=str, help='Algorithm name')
ap.add_argument('--migration', action='store_true', help='Migration enabled')
args = ap.parse_args()

# load output data
file_path = config.out_path +f"assignments_{args.algorithm}{'_migration'*args.migration}.json"
with open(file_path, "r") as f:
    assignments = json.load(f)["assignments"]


# Extract data for plotting
timestamps = list(assignments.keys())
power_values = [sum([job['power'] for job in assignments[timestamp]])for timestamp in timestamps]
carbon_values = [sum([job['carbon']/10**3  for job in assignments[timestamp]]) for timestamp in timestamps]
water_values = [sum([job['water'] for job in assignments[timestamp]]) for timestamp in timestamps]
land_use_values = [sum([job['land_use']/10**3  for job in assignments[timestamp]]) for timestamp in timestamps]

# Plotting
plt.figure(figsize=(14, 8))

plt.subplot(2, 2, 1)
plt.bar(timestamps, power_values, color='purple')
plt.xticks(ticks=timestamps, labels=[ts.split('T')[1][:5] for ts in timestamps], rotation=90)
plt.title('Power Usage')
plt.xlabel('Timestamp')
plt.ylabel('Power (kW)')

plt.subplot(2, 2, 2)
plt.bar(timestamps, carbon_values, color='green')
plt.xticks(ticks=timestamps, labels=[ts.split('T')[1][:5] for ts in timestamps], rotation=90)
plt.title('Carbon Emissions')
plt.xlabel('Timestamp')
plt.ylabel('Carbon (kgCO2)')

plt.subplot(2, 2, 3)
plt.bar(timestamps, water_values, color='blue')
plt.xticks(ticks=timestamps, labels=[ts.split('T')[1][:5] for ts in timestamps], rotation=90)
plt.title('Water Usage')
plt.xlabel('Timestamp')
plt.ylabel('Water (l)')

plt.subplot(2, 2, 4)
plt.bar(timestamps, land_use_values, color='red')
plt.xticks(ticks=timestamps, labels=[ts.split('T')[1][:5] for ts in timestamps], rotation=90)
plt.title('Land Use')
plt.xlabel('Timestamp')
plt.ylabel('Carbon Capture Loss (kgCO2)')

plt.tight_layout()

if not os.path.exists(config.plot_path):
    os.makedirs(config.plot_path)
out_path = config.plot_path + f"plot_{args.algorithm}{'_migration'*args.migration}.png"
plt.savefig(out_path)