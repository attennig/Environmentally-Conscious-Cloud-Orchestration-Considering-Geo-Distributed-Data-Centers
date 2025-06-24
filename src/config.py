from src.models.objectives import *
from src.models.algorithms import *

seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
d_i = "2025-05-12T00:00:00.000Z"
d_f = "2025-05-14T23:00:00.000Z"



report_folder = "./data/reports"
experiments_folder = "./data/experiments"
output_folder = "./out"

"""
in_path = f"./data/{d_i}-{d_f}/"
out_path = f"./out/{d_i}-{d_f}/"
plot_path = f"./plot/figures/{d_i}-{d_f}/"
raw_data_path = f"./data_preprocessing/"
"""

algorithm = {
    #"random": (get_random_dc, eval_name),
    "carbon_greedy": (greedy_assignment, eval_carbon),
    "water_greedy": (greedy_assignment, eval_water),
    "land_use_greedy": (greedy_assignment, eval_land_use),
    "preference_based_greedy": (greedy_assignment, eval_preference),
    "carbon_opt": (optimize_assignment, eval_carbon),
    "water_opt": (optimize_assignment, eval_water),
    "land_use_opt": (optimize_assignment, eval_land_use),
    "preference_based_opt": (optimize_assignment, eval_preference),

}

from src.plot.colors import IBM_color_blind_palette, IBM_color_blind_palette_shadow
colors = {
    #"random": "gray",
    "carbon_greedy": IBM_color_blind_palette[1],
    "water_greedy": IBM_color_blind_palette[0],
    "land_use_greedy": IBM_color_blind_palette[4],
    "preference_based_greedy": IBM_color_blind_palette[2],
   "carbon_opt": IBM_color_blind_palette[1],
    "water_opt": IBM_color_blind_palette[0],
    "land_use_opt": IBM_color_blind_palette[4],
    "preference_based_opt": IBM_color_blind_palette[2]
}

colors_shadow = {
    #"random": "gray",
    "carbon_greedy": IBM_color_blind_palette_shadow[1],
    "water_greedy": IBM_color_blind_palette_shadow[0],
    "land_use_greedy": IBM_color_blind_palette_shadow[4],
    "preference_based_greedy": IBM_color_blind_palette_shadow[2],
   "carbon_opt": IBM_color_blind_palette_shadow[1],
    "water_opt": IBM_color_blind_palette_shadow[0],
    "land_use_opt": IBM_color_blind_palette_shadow[4],
    "preference_based_opt": IBM_color_blind_palette_shadow[2]
}


marker = {
    #"random": "gray",
    "carbon_greedy": "o",
    "water_greedy": "o",
    "land_use_greedy": "o",
    "preference_based_greedy": "o",
   "carbon_opt": "*",
    "water_opt": "*",
    "land_use_opt": "*",
    "preference_based_opt": "*"
}


names = {
    
    "carbon_greedy": "Carbon-Only Greedy",
    "water_greedy": "Water-Only Greedy",
    "land_use_greedy": "Land-Use-Only Greedy",
    "preference_based_greedy": "Preference-based Greedy",
    "carbon_opt": "Carbon-Only Optimization",
    "water_opt": "Water-Only Optimization",
    "land_use_opt": "Land-Use-Only Optimization",
    "preference_based_opt": "Preference-based Optimization",

}


lable_size = 9
