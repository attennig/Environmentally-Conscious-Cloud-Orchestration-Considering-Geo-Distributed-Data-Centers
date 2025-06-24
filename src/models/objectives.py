# carbon greedy
get_dc_by_min_carbon = lambda timestamp, job, dcs:  sorted(dcs, key=lambda dc: eval_carbon(timestamp, job, dc))[0]
eval_carbon = lambda timestamp, job, dc: dc.get_carbon_emissions(timestamp, float(job["expected_power_per_hour"]))

# water greedy
get_dc_by_min_water = lambda timestamp, job, dcs: sorted(dcs, key=lambda dc: eval_water(timestamp, job, dc))[0]
eval_water = lambda timestamp, job, dc: dc.get_water_use(timestamp, float(job["expected_power_per_hour"]))

# land use greedy
get_dc_by_min_land_use = lambda timestamp, job, dcs: sorted(dcs, key=lambda dc: eval_land_use(timestamp, job, dc))[0]
eval_land_use = lambda timestamp, job, dc : dc.get_carbon_capture_loss(timestamp, float(job["expected_power_per_hour"]))

# preference_based greedy
get_dc_by_preference = lambda timestamp, job, dcs: sorted(dcs, key=lambda dc: eval_preference(timestamp, job, dc))[0]
eval_preference = lambda timestamp, job, dc: job["carbon_preference"] * dc.get_carbon_emissions(timestamp, float(job["expected_power_per_hour"])) + job["water_preference"] * dc.get_water_use(timestamp, float(job["expected_power_per_hour"])) + job["land_use_preference"] * dc.get_carbon_capture_loss(timestamp, float(job["expected_power_per_hour"]))
