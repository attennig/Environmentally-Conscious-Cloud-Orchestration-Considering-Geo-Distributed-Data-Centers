from models.objectives import *

d_i = "2024-12-16T13:00:00.000Z"
d_f = "2024-12-17T12:00:00.000Z"

in_path = f"./data/{d_i}-{d_f}/"
out_path = f"./out/{d_i}-{d_f}/"
plot_path = f"./plot/figures/{d_i}-{d_f}/"

algorithm = {
    #"random": (get_random_dc, eval_name),
    "carbon_greedy": (get_dc_by_min_carbon, eval_carbon),
    "water_greedy": (get_dc_by_min_water, eval_water),
    "land_use_greedy": (get_dc_by_min_land_use, eval_land_use),
    "preference_based": (get_dc_by_preference, eval_preference)
}


colors = {
    #"random": "gray",
    "carbon_greedy": "#004D40",
    "water_greedy": "#1E88E5",
    "land_use_greedy": "#FFC107",
    "preference_based": "#D81B60"
}


names = {
    
    "carbon_greedy": "Carbon-Only Optimization",
    "water_greedy": "Water-Only Optimization",
    "land_use_greedy": "Land-Use-Only Optimization",
    "preference_based": "Preference-based Optimization"
}