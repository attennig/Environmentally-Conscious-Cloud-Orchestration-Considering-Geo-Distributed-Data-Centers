#!/bin/bash

# List of algorithms
algorithms=("carbon_opt" "water_opt" "land_use_opt" "preference_based_opt")

experiments=("cp_exp10_100MW" "meta_exp10")

for experiment in "${experiments[@]}"
do
    # Loop over each algorithm
    for algorithm in "${algorithms[@]}"
    do
        echo "Making plots of experiment with $algorithm"
        # Add your experiment command here, for example:
        python3 -m src.plot.migration_comparison_single_experiment --algorithm $algorithm --experiment_name  $experiment

    done
    echo "${algorithms[@]}"
    python3 -m src.plot.algorithm_comparison --algorithms "${algorithms[@]}" --migration --experiment_name $experiment
done


#python3 -m src.plot.migration_comparison_single_experiment --algorithm preference_based_opt --experiment_name  meta_exp10
#python3 -m src.plot.algorithm_comparison --algorithms carbon_opt water_opt land_use_opt preference_based_opt --migration --experiment_name cp_exp10_100MW