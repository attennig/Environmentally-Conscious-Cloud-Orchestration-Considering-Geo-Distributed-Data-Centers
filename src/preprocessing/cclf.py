tonsha2kgsqm = lambda x: x * 100
acre2sqm = lambda x: x * 4046.86

us_carbon_sequestration_factor = {
    "R1": 5.83*10**12/acre2sqm(24.4*10**6),  # Northern Region https://www.fs.usda.gov/sites/default/files/northern-region-carbon-assessment.pdf 5.83 Tg carbon/year (page 19) 22.4 million acres (page 10)
    "R2": 1.02*10**12/acre2sqm(15.6*10**6),  # Rocky Mountain Region https://www.fs.usda.gov/sites/default/files/rocky-mountain-region-carbon-assessment.pdf 1.02 Tg carbon/year (page 19) 15.6 million acres (page 10)
    "R3": 0,  # Southwestern Region https://www.fs.usda.gov/sites/default/files/southwestern-region-carbon-assessment.pdf -1.46 Tg carbon/year (page 19) 15.2 million acres (page 10) 
    "R4": 1.91*10**12/acre2sqm(15.2*10**6),  # Intermountain Region https://www.fs.usda.gov/sites/default/files/intermountain-region-carbon-assessment.pdf 1.91 Tg carbon/year (page 19) 22.6 million acres (page 10)
    "R5": 0,  # Pacific Southwest Region https://www.fs.usda.gov/sites/default/files/pacific-southwest-carbon-assessment.pdf 14.5 million acres (page 10) -1.48 Tg carbon/year (page 19)
    "R6": 7.63*10**12/acre2sqm(22.7*10**6),  # Pacific Northwest Region https://www.fs.usda.gov/sites/default/files/pacific-northwest-region-carbon-assessment.pdf 7.63 Tg carbon/year (page 19) 22.7 million acres (page 10) 
    "R8": 9.22*10**12/acre2sqm(13.8*10**6),  # Southern Region https://www.fs.usda.gov/sites/default/files/southern-region-carbon-assessment.pdf 9.22 Tg carbon/year (page 19) 13.8 million acres (page 10) 
    "R9": 8.44*10**12/acre2sqm(12*10**6),  # Eastern Region https://www.fs.usda.gov/sites/default/files/eastern-region-carbon-assessment.pdf 8.44 Tg carbon/year (page 19)  12 million acres (page 10)
    "R10": 0.71*10**12/acre2sqm(10*4**6)  # Alaska Region https://www.fs.usda.gov/sites/default/files/alaska-region-carbon-assessment.pdf  0.71 Tg carbon/year (page 19) 10.4 million acres (page 10)
    # Note: There is no active R7. It was merged into others.
} # gCO2/m^2/year


us_forest_service_regions = {
    # Region 1 – Northern
    "Montana": "R1",
    "North Dakota": "R1",
    "Northern Idaho": "R1",

    # Region 2 – Rocky Mountain
    "Colorado": "R2",
    "Wyoming": "R2",
    "Nebraska": "R2",
    "Kansas": "R2",
    "South Dakota": "R2",

    # Region 3 – Southwestern
    "Arizona": "R3",
    "New Mexico": "R3",

    # Region 4 – Intermountain
    "Nevada": "R4",
    "Utah": "R4",
    "Southern Idaho": "R4",
    "Western Wyoming": "R4",

    # Region 5 – Pacific Southwest
    "California": "R5",
    "Hawaii": "R5",

    # Region 6 – Pacific Northwest
    "Oregon": "R6",
    "Washington": "R6",

    # Region 8 – Southern
    "Texas": "R8",
    "Oklahoma": "R8",
    "Kentucky": "R8",
    "Tennessee": "R8",
    "Mississippi": "R8",
    "Alabama": "R8",
    "Georgia": "R8",
    "South Carolina": "R8",
    "North Carolina": "R8",
    "Florida": "R8",
    "Louisiana": "R8",
    "Arkansas": "R8",
    "Virginia": "R8",

    # Region 9 – Eastern
    "Minnesota": "R9",
    "Wisconsin": "R9",
    "Michigan": "R9",
    "Missouri": "R9",
    "Illinois": "R9",
    "Indiana": "R9",
    "Ohio": "R9",
    "Iowa": "R9",
    "West Virginia": "R9",
    "Pennsylvania": "R9",
    "New York": "R9",
    "Vermont": "R9",
    "New Hampshire": "R9",
    "Maine": "R9",
    "Massachusetts": "R9",
    "Connecticut": "R9",
    "Rhode Island": "R9",
    "New Jersey": "R9",
    "Delaware": "R9",
    "Maryland": "R9",

    # Region 10 – Alaska
    "Alaska": "R10",

    
}

"""# Territories (typically under R5 or other special units)
    "Washington D.C.": "R9",
    "Puerto Rico": "R8",
    "Guam": "R5",
    "American Samoa": "R5",
    "Northern Mariana Islands": "R5",
    "U.S. Virgin Islands": "R8"
"""



loss_factors = {
    "Australia": tonsha2kgsqm(3.9), #tons/ha/year
    # Australia https://www.uwa.edu.au/news/Article/2022/March/In-20-years-of-studying-how-ecosystems-absorb-carbon-heres-why-were-worried-about-a-tipping-point-of-collapse every hectare of Australia’s temperate forests absorbs 3.9 tonnes of carbon in a year, according to OzFlux data
    "Denmark": tonsha2kgsqm(2.2*10**6/640835), 
    # Denmark https://tracker.carbongap.org/regional-analysis/national/denmark/?printThis=true&nonce=89c5214e15 Annual Removals: 2.2 Mt CO2 per year from forests https://en.lbst.dk/nature-and-forestry/forestry#:~:text=Facts%20on%20the%20Danish%20forests,Forest%20area There are officially 640,835 ha of forest in Denmark
    "Sweden": tonsha2kgsqm(2), # tons/ha/year
    # Sweden https://pub.norden.org/us2024-428/annex-4-carbon-stock-and-sink-data-of-trees-in-urban-areas-in-the-context-of-building-climate-reporting.html " For example, in the Stockholm municipality, the carbon sink in forests and soil was estimated to be -35 kt CO2e per year, corresponding to slightly below 2 t CO2e per hectare per year (Lindahl & Lundblad, 2022)"
    "Ireland": tonsha2kgsqm(3.36), # tons/ha/year
    # Ireland https://www.woodenergy.ie/media/coford/content/publications/projectreports/cofordconnects/CarbonSequestration.pdf
    "Iowa": us_carbon_sequestration_factor[us_forest_service_regions["Iowa"]], 
    "Illinois": us_carbon_sequestration_factor[us_forest_service_regions["Illinois"]],
    "Utah": us_carbon_sequestration_factor[us_forest_service_regions["Utah"]],
    "North Carolina": us_carbon_sequestration_factor[us_forest_service_regions["North Carolina"]],
    "Texas": us_carbon_sequestration_factor[us_forest_service_regions["Texas"]],
    "Tennessee": us_carbon_sequestration_factor[us_forest_service_regions["Tennessee"]],
    "Virginia": us_carbon_sequestration_factor[us_forest_service_regions["Virginia"]],
    "Alabama": us_carbon_sequestration_factor[us_forest_service_regions["Alabama"]],
    "New Mexico": us_carbon_sequestration_factor[us_forest_service_regions["New Mexico"]],
    "Ohio": us_carbon_sequestration_factor[us_forest_service_regions["Ohio"]],
    "Oregon": us_carbon_sequestration_factor[us_forest_service_regions["Oregon"]],
    "Nebraska": us_carbon_sequestration_factor[us_forest_service_regions["Nebraska"]],
    "Georgia": us_carbon_sequestration_factor[us_forest_service_regions["Georgia"]],
    "California": us_carbon_sequestration_factor[us_forest_service_regions["California"]]
} # kgCO2/m^2/year