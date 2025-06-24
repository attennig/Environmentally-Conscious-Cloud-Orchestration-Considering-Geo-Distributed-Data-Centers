import src.config as config
def optimize_assignment(datacenters, dc_max_capacity, timestamp, eval_objective, jobs, utilization, prev):
        from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpBinary, LpInteger, GUROBI, LpStatusInfeasible, PULP_CBC_CMD
        d_index = {
            dc.name: i
            for i, dc in enumerate(datacenters)
        }
        d_obj = {
            i: dc
            for i, dc in enumerate(datacenters)
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
        N = len(datacenters)  # Number of data centers
        M = len(jobs)  # Number of jobs
        
        max_capacity = dc_max_capacity

        # Data center capacity (max number of jobs per DC)
        P_max = {d: max_capacity - utilization[d_obj[d].name] for d in range(N)}

        # --------------------
        # Decision Variables
        # --------------------
        x = LpVariable.dicts("x", [(j, d) for j in range(M) for d in range(N)], cat=LpBinary)
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
            model.writeLP(f"{config.output_folder}/debug_model.lp")
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




def greedy_assignment(datacenters, dc_max_capacity, timestamp, eval_objective, jobs, utilization, prev):
    pass