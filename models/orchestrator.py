import config
class Orchestrator:
    def __init__(self, datacenters, migration_enabled=False):
        self.datacenters = datacenters
        self.migration_enabled = migration_enabled
        self.dc_max_capacity = 5

    def get_dc_by_name(self, name):
        return [dc for dc in self.datacenters if dc.name == name][0]
    
        

    def optimize_assignment(self, timestamp, eval_objective, jobs, utilization, prev):
        from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpBinary, LpInteger, GUROBI, LpStatusInfeasible, PULP_CBC_CMD
        d_index = {
            dc.name: i
            for i, dc in enumerate(self.datacenters)
        }
        d_obj = {
            i: dc
            for i, dc in enumerate(self.datacenters)
        }
        j_obj = {
            i : job
            for i, job in enumerate(jobs)
        }
        j_index = {
            job["job_id"] : i
            for i, job in enumerate(jobs)
        }

        # --------------------
        # Problem Definition
        # --------------------
        model = LpProblem("Sustainable_Cloud_Orchestration", LpMinimize)

        # --------------------
        # Sets and Parameters
        # --------------------
        N = len(self.datacenters)  # Number of data centers
        M = len(jobs)  # Number of jobs

        
        
        
        max_capacity = self.dc_max_capacity

        # Data center capacity (max number of jobs per DC)
        P_max = {d: max_capacity - utilization[d_obj[d].name] for d in range(N)}


        # --------------------
        # Decision Variables
        # --------------------
        x = LpVariable.dicts("x", [(j, d) for j in range(M) for d in range(N)], cat=LpBinary)
        #m = LpVariable.dicts("m", [j for j in range(M) ], cat=LpBinary) # m[j] = 1 --> the job has been migrated
        #n = LpVariable.dicts("n", [d for d in range(N) ], cat=LpInteger) # n[d] = the number of jobs that have been migrated from d

        # --------------------
        # Objective Function: Minimize Sustainability Impact
        # --------------------
        model += lpSum( eval_objective(timestamp=timestamp, job=j_obj[j], dc=d_obj[d]) * x[j,d]
                    for d in range(N) for j in range(M)
                    )
        
        # 1. Each job is assigned to exactly one data center
        for j in range(M):
            model += lpSum(x[j, d] for d in range(N)) == 1
        # 2. Migration trigger (10% improvement rule) and logic 
        for j in range(M):
            dc_prev = prev[j_obj[j]["job_id"]]
            print(f"job: {j} --> {dc_prev}")
            if dc_prev != None: 
                d_prev = d_index[dc_prev.name]
                for d in range(N):
                    if d_prev != d:
                        prev_impact = eval_objective(timestamp=timestamp, job=j_obj[j], dc=d_obj[d_prev])
                        new_impact = eval_objective(timestamp=timestamp, job=j_obj[j], dc=d_obj[d])
                        model += x[j,d] * new_impact <= 0.9 * prev_impact 
        # 3. Capacity constraint: Each data center must not exceed its job limit
        for d in range(N):
            model += lpSum(x[j, d] for j in range(M) if d_obj[d] != prev[j_obj[j]["job_id"]]) <= P_max[d] 


        model.solve(GUROBI(msg=True))

        if model.status == LpStatusInfeasible:
            model.writeLP(f"{config.out_path}debug_model.lp")
            import sys
            sys.exit(-1)

        assignment = []
        for d in range(N):
            for j in range(M):
                if x[j, d].value() == 1:
                    assignment.append(
                        {
                            "job": j_obj[j],
                            "datacenter": d_obj[d]
                        }
                    )
        return assignment
                    
                    


    def orchestrationMILP(self, eval_objective, requests):
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
            assignments_t = self.optimize_assignment(timestamp, eval_objective, jobs_to_assign, utilization, curr_assignment)
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