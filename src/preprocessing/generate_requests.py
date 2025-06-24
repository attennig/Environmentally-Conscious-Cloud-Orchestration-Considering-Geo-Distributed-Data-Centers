from datetime import timedelta, datetime
from numpy import random
import json
from src.utils import str_to_date, date_to_str, get_timestamps
import src.config as config


def get_random_job(j_id: int, remaining_time: datetime, n_users: int, dc_names: list[str]):
    u_id = int(random.choice([i for i in range(n_users)]))
    power = float(round(random.uniform(0.5, 10), 2))  # kWh
    lifetime = int(random.uniform(1, min(remaining_time,5)))  # hours
    dc_name = str(random.choice(dc_names))
    return {
        'job_id': j_id,
        'user_id': u_id,
        'expected_power_per_hour': power,
        'expected_lifetime': lifetime,
        'request_source': dc_name
    }

def generate_requests(t_i: datetime, t_f: datetime, n_jobs: int, n_users: int, dc_names: list[str]):
    timestamps = get_timestamps(t_i, t_f, timedelta(hours=1))
    data = {
        date_to_str(t): []
        for t in timestamps
    }
    for i in range(n_jobs):
        random_time = random.choice(timestamps)
        remaining_time = (t_f - random_time).total_seconds()/ 3600 + 1 # hours # +1 is the last hour
        data[date_to_str(random_time)].append(get_random_job(i,remaining_time, n_users, dc_names))

    return data


def generate_requests_poisson(t_i: datetime, t_f: datetime, n_users: int, dc_names: list[str]):
    timestamps = get_timestamps(t_i, t_f, timedelta(hours=1))
    data = {
        date_to_str(t): []
        for t in timestamps
    }
    job_arrivals = random.poisson(lam = 10, size = len(timestamps))
    job_count = 0
    for i, t in enumerate(timestamps):
        remaining_time = (t_f - t).total_seconds()/ 3600 + 1 # hours # +1 is the last hour
        for j in range(job_arrivals[i]):
            data[date_to_str(t)].append(get_random_job(job_count,remaining_time, n_users, dc_names))
            job_count += 1
    
    return data

import argparse, os

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--init_time', type=str, help='Initial time of simulation')
    ap.add_argument('--final_time', type=str, help='Final time of simulation')
    #ap.add_argument('--n_jobs', type=int, help='Number of jobs')
    ap.add_argument('--n_users', type=int, help='Number of users')
    ap.add_argument('--seed', type=int, help='Seed')
    

    args = ap.parse_args()

    random.seed(seed=args.seed)

    in_path = f"{config.experiments_folder}/{args.init_time}-{args.final_time}/processed/"

    dc_names = []   
    for file in os.listdir(in_path):
        if "meta_" in file or "aws_" in file or "azure_" in file or "gcp_" in file:
            name = file.split(".")[0]
            dc_names.append(name)

    print(dc_names)
    data = generate_requests_poisson(
        str_to_date(args.init_time), 
        str_to_date(args.final_time), 
        #args.n_jobs, 
        args.n_users, 
        dc_names)

    with open(f'{in_path}requests{args.seed}.json', 'w') as f:
        json.dump(data, f, indent=4)

#python -m src.preprocessing.generate_requests --init_time 2025-05-12T00:00:00.000Z --final_time 2025-05-14T23:00:00.000Z --n_users 3
