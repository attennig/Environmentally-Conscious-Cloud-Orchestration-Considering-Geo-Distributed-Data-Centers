import os, json, argparse

from models.datacenter import Datacenter
from models.orchestrator import Orchestrator
import config

# args
ap = argparse.ArgumentParser()
ap.add_argument('--algorithm', type=str, help='Algorithm name')
ap.add_argument('--migration', action='store_true', help='Migration enabled')
args = ap.parse_args()

# Load data
if not os.path.exists(config.out_path):
    os.makedirs(config.out_path)
assert os.path.exists(config.out_path)
datacenters = []
dc_capacity = 5
for file in os.listdir(config.in_path):
    if "meta_" in file or "google_" in file or "azure_" in file:
        with open(config.in_path + file, "r") as f:
            data = json.load(f)
            name = file.split(".")[0]
        datacenters.append(Datacenter(name, data, dc_capacity))

with open(config.in_path + "users.json", "r") as f:
    users = json.load(f)

with open(config.in_path + "requests.json", "r") as f:
    requests = json.load(f)

for requests_t in requests.values():
    for request in requests_t:
        assert request["request_source"] in [dc.name for dc in datacenters]
        request["carbon_preference"] = users[str(request["user_id"])]["carbon"]
        request["water_preference"] = users[str(request["user_id"])]["water"]
        request["land_use_preference"] = users[str(request["user_id"])]["land_use"]

# orchestration
orch = Orchestrator(datacenters=datacenters, migration_enabled=args.migration)
objective = config.algorithm[args.algorithm][0]
eval_objective = config.algorithm[args.algorithm][1]
out = orch.orchestrationMILP(eval_objective=eval_objective, requests=requests)

# save output
with open(config.out_path +f"assignments_{args.algorithm}{'_migration'*args.migration}.json", "w") as f:
    json.dump(out, f)
