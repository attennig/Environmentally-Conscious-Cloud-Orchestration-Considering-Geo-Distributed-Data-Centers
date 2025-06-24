import os, json, argparse
import src.models.datacenter as datacenter
import src.models.orchestrator as orchestrator
import src.config as config

# args
ap = argparse.ArgumentParser()
ap.add_argument('--algorithm', type=str, help='Algorithm name')
ap.add_argument('--seed', type=int, help='Seed')

ap.add_argument('--migration', action='store_true', help='Migration enabled')

args = ap.parse_args()

# Load data
if not os.path.exists(config.output_folder):
    os.makedirs(config.output_folder)
assert os.path.exists(config.output_folder)
datacenters = []
dc_capacity = 5


experiment_data_folder = f"{config.experiments_folder}/{config.d_i}-{config.d_f}/processed/"
datacenters = {}
for dc_name in os.listdir(experiment_data_folder):
    if not os.path.isdir(experiment_data_folder+"/"+dc_name): 
        continue
    datacenters[dc_name] = datacenter.Datacenter(
        name=dc_name,
        data=json.load(open(experiment_data_folder+dc_name+"/profile.json", "r")), 
        capacity=dc_capacity
    )

with open(experiment_data_folder + "users.json", "r") as f:
    users = json.load(f)

with open(experiment_data_folder + f"requests{args.seed}.json", "r") as f:
    requests = json.load(f)

for requests_t in requests.values():
    for request in requests_t:
        assert request["request_source"] in [dc_name for dc_name in datacenters.keys()]
        request["carbon_preference"] = users[str(request["user_id"])]["carbon"]
        request["water_preference"] = users[str(request["user_id"])]["water"]
        request["land_use_preference"] = users[str(request["user_id"])]["land_use"]

# orchestration
orch = orchestrator.Orchestrator(datacenters=list(datacenters.values()), migration_enabled=args.migration)
method = config.algorithm[args.algorithm][0]
eval_objective = config.algorithm[args.algorithm][1]
out = orch.orchestration(method=method, eval_objective=eval_objective, requests=requests)

# save output
out_path = f"{config.output_folder}/{config.d_i}-{config.d_f}"
if not os.path.exists(out_path):
    os.makedirs(out_path)
with open(f"{out_path}/{args.seed}_assignments_{args.algorithm}{'_migration'*args.migration}.json", "w") as f:
    json.dump(out, f)
