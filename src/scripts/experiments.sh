#!/bin/bash

# List of algorithms
algorithms=("carbon_opt" "water_opt" "land_use_opt" "preference_based_opt")
seeds=(1 2 3 4 5 6 7 8 9 10)
# Loop over each algorithm
for algorithm in "${algorithms[@]}"
do
    for seed in "${seeds[@]}"
    do
        echo "Running experiment with $algorithm and seed $seed"
        python3 -m src.scripts.experiment --algorithm $algorithm --seed $seed --migration
        python3 -m src.scripts.experiment --algorithm $algorithm --seed $seed
    done

done
