#!/bin/bash

# List of algorithms
algorithms=("carbon_greedy" "water_greedy" "land_use_greedy" "preference_based")

# Loop over each algorithm
for algorithm in "${algorithms[@]}"
do
    echo "Making plots of experiment with $algorithm"
    # Add your experiment command here, for example:
    #python3 -m plot.src.single_experiment --algorithm $algorithm
    #python3 -m plot.src.single_experiment --algorithm $algorithm --migration
    python3 -m plot.src.migration_comparison_single_experiment --algorithm $algorithm
done
python3 -m plot.src.algorithm_comparison --migration
#python3 -m plot.src.algorithm_comparison 

python3 -m plot.src.plot_wue_IR_TX --state Texas
python3 -m plot.src.plot_wue_IR_TX --state Ireland

