
class Orchestrator:
    def __init__(self, datacenters, migration_enabled=False):
        self.datacenters = datacenters
        self.migration_enabled = migration_enabled
        self.dc_max_capacity = 5

    def get_dc_by_name(self, name):
        return [dc for dc in self.datacenters if dc.name == name][0]
    

    def orchestration(self, method, eval_objective, requests):
        assignments = {timestamp: [] for timestamp in requests.keys()}
        utilization = {
            dc.name : 0
            for dc in self.datacenters
        }
        curr_assignment = {
            job["job_id"] : None # Datacenter obj
            for t, jobs in requests.items()
            for job in jobs 
        }
        running_jobs = []
        for timestamp, jobs in requests.items():
            # 1. Remove finshed jobs
            finished_jobs = [job for job in running_jobs if job["expected_lifetime"] <= 0]
            for f_job in finished_jobs:
                dc_assigned = curr_assignment[f_job["job_id"]]
                utilization[dc_assigned.name] -= 1
                running_jobs.remove(f_job)
                curr_assignment[f_job["job_id"]] = None
            # 2. Optimize assignment
            jobs_to_assign = jobs+running_jobs if self.migration_enabled else jobs
            assignments_t = method(self.datacenters, self.dc_max_capacity, timestamp, eval_objective, jobs_to_assign, utilization, curr_assignment)
            # 3. Update curr_assignment and utilization and running_jobs
            for assignment in assignments_t:
                assiged_dc = assignment["datacenter"]
                assigned_job = assignment["job"]

                if self.migration_enabled:
                    if curr_assignment[assigned_job["job_id"]]:
                        if curr_assignment[assigned_job["job_id"]] != assiged_dc:
                            print(f"MIGRATION {self.migration_enabled}")
                            print(f"{assigned_job["job_id"]} MIGRATED from {curr_assignment[assigned_job["job_id"]].name} to {assiged_dc.name}")
                        utilization[curr_assignment[assigned_job["job_id"]].name] -= 1
                        running_jobs.remove(assigned_job)


                running_jobs.append(assigned_job)
                curr_assignment[assigned_job["job_id"]] = assiged_dc
                utilization[assiged_dc.name] += 1
            

            # 4. Advance time
            for r_job in running_jobs:
                assiged_dc = curr_assignment[r_job["job_id"]]
                assignments[timestamp].append({
                            "job_id": r_job["job_id"],
                            "datacenter": assiged_dc.name,
                            "power": r_job["expected_power_per_hour"],
                            "carbon": assiged_dc.get_carbon_emissions(timestamp, float(r_job["expected_power_per_hour"])),
                            "water": assiged_dc.get_water_use(timestamp, float(r_job["expected_power_per_hour"])),
                            "land_use": assiged_dc.get_carbon_capture_loss(timestamp, float(r_job["expected_power_per_hour"])),
                        })
                r_job["expected_lifetime"] -= 1

        return {
            "assignments": assignments
        }