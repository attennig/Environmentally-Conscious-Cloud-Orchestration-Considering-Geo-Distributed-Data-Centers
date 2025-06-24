import numpy as np
import src.config as config
def get_datapoints(metric, assignments, timestamps):
    data = {
        timestamp: [] for timestamp in timestamps
    }

    dp_mean, dp_std = [],  []
    for seed in config.seeds:
        for timestamp, jobs in assignments[seed].items():
            data[timestamp].append(sum([job[metric] for job in jobs]))
    for timestamp in timestamps:
        dp_mean.append(np.mean(data[timestamp]))
        dp_std.append(np.std(data[timestamp]))

    return dp_mean, dp_std