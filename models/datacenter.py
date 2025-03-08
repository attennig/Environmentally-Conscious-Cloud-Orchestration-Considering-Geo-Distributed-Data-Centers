import config
class Profile:
    def __init__(self, data):
        self.PUE = float(data["static"]["PUE"])
        self.WUE = float(data["static"]["WUE"])
        self.WSF = float(data["static"]["WSF"])
        self.LUE = float(data["static"]["LUE"])

        # Grid and time dependent data
        self.CI = {
            entry["timestamp"]: float(entry["carbon_intensity"])
            for entry in data["dynamic"]
        } # gCO2/kWh
        self.EWIF = {
            entry["timestamp"]: float(entry["water_intensity"])
            for entry in data["dynamic"]
        } # l/kWh
        self.ELIF = {
            entry["timestamp"]: float(entry["land_use_intensity"])
            for entry in data["dynamic"]
        } # m2/kWh

        self.WUE_dynamic = {
            entry["timestamp"]: float(entry["wue"])
            for entry in data["dynamic"]
        } # l/kWh


        

class Datacenter:
    def __init__(self, name, data, capacity):
        self.name = name
        self.profile = Profile(data)
        self.capacity = capacity

    def get_carbon_emissions(self, timestamp: str, energy_consumption: float) -> float:
        return self.profile.CI[timestamp] * (energy_consumption * self.profile.PUE)
    
    def get_water_use(self, timestamp: str, energy_consumption: float) -> float:
        off_site = self.profile.EWIF[timestamp] * (energy_consumption * self.profile.PUE) 
        on_site = self.profile.WUE * energy_consumption
        return (off_site + on_site) * self.profile.WSF

    
    def get_carbon_capture_loss(self, timestamp: str, energy_consumption: float) -> float:
        carbon_capture_loss = lambda usage_m2_per_kWh : usage_m2_per_kWh * 0.5*10**3 # = annual_absorption_rate_per_m2  gCO2/m*2 --> gCO2/kWh
        off_site = carbon_capture_loss(self.profile.ELIF[timestamp]) * (energy_consumption * self.profile.PUE) 
        on_site = carbon_capture_loss(self.profile.LUE) * energy_consumption
        return off_site + on_site
    

"""
    def get_water_use(self, timestamp: str, energy_consumption: float) -> float:
        if config.wue_type == "dynamic":
            return self.get_water_use_dynamic(timestamp, energy_consumption)
        return self.get_water_use_static(timestamp, energy_consumption)

    
    
    def get_water_use_dynamic(self, timestamp: str, energy_consumption: float) -> float:
        off_site = self.profile.EWIF[timestamp] * (energy_consumption * self.profile.PUE) 
        on_site = self.profile.WUE_dynamic[timestamp] * energy_consumption
        return (off_site + on_site) * self.profile.WSF
"""