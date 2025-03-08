#!/bin/bash

# List of algorithms
algorithms=("carbon_greedy" "water_greedy" "land_use_greedy" "preference_based")

# Loop over each algorithm
for algorithm in "${algorithms[@]}"
do
    echo "Running experiment with $algorithm"
    # Add your experiment command here, for example:
    python3 -m experiment --algorithm $algorithm --migration
    python3 -m experiment --algorithm $algorithm
done
