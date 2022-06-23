from os import  rename
import json
from _helper import get_total_experiments, get_experiment_files, get_experiment_benchmark, get_experiment_configuration, get_experiment_demand
import pandas as pd

temp_dir = './temp'
docs_dir = './docs'
results_dir = './results'

exp_actual = 0
for experiment_id in range(0, get_total_experiments()):
    files = get_experiment_files(experiment_id)
    if len(files) == 0:
        continue
    if experiment_id == exp_actual:
        exp_actual += 1
        continue
    print('Moving experiment:', experiment_id,'to', exp_actual)
    for file in files:
        actual_file = '{}/{}'.format(results_dir, file)
        new_file = '{}/{}'.format(results_dir, file.replace('exp{}_'.format(experiment_id), 'exp{}_'.format(exp_actual)).replace('exp{}-'.format(experiment_id), 'exp{}-'.format(exp_actual)))
        rename(actual_file, new_file)
    exp_actual += 1

for experiment_id in range(0, get_total_experiments(temp_dir)):
    files = get_experiment_files(experiment_id, temp_dir)
    if len(files) == 0:
        continue
    print('Moving experiment:', experiment_id, 'to', exp_actual)
    for file in get_experiment_files(experiment_id, temp_dir):
        actual_file = '{}/{}'.format(temp_dir, file)
        new_file = '{}/{}'.format(results_dir, file.replace('exp{}_'.format(experiment_id), 'exp{}_'.format(exp_actual)).replace('exp{}-'.format(experiment_id), 'exp{}-'.format(exp_actual)))
        rename(actual_file, new_file)
    exp_actual += 1

f = open("{}/expID.txt".format(results_dir), "w")
f.write(str(exp_actual))
f.close()
        
results = {}
results_times = {}
for experiment_id in range(0, exp_actual):
    demand = get_experiment_demand(experiment_id)
    total_demand = len(demand)
    if not total_demand:
        continue
    print('Experiment:', experiment_id)
    print('Results:', total_demand)
    benchmark_info, partitions = get_experiment_benchmark(experiment_id)
    print('Benchmark:', benchmark_info)
    if 'uc4' in benchmark_info and total_demand < 10:
        print('Ignored, benchmark unfinished...\n')
        continue
    if ('uc1' in benchmark_info or 'uc2' in benchmark_info or 'uc3' in benchmark_info) and total_demand < 13:
        print('Ignored, benchmark unfinished...\n')
        continue

    print('\n')
    files = list(filter(lambda file: '.csv' in file and 'lag-trend' in file, get_experiment_files(experiment_id)))
    execution_configuration = get_experiment_configuration(experiment_id)
    if benchmark_info not in results:
        results[benchmark_info] = {}
    if partitions not in results[benchmark_info]:
        results[benchmark_info][partitions] = {}
    not_finished = False
    for line in demand:
        if 'load,resources' in line:
            continue
        values = line.strip().split(',')
        if len(values) < 2 or values[1]=='-2147483648':
            not_finished = True
            break
        if str(values[0]) not in results[benchmark_info][partitions]:
            results[benchmark_info][partitions][values[0]] = []
        results[benchmark_info][partitions][values[0]].append(int(values[1]))
    if not_finished:
        continue

    times = []
    for file in files:
        result = pd.read_csv('./results/{}'.format(file))
        times += list(result['timestamp'])
    benchmark_info, partitions = get_experiment_benchmark(experiment_id)
    if benchmark_info not in results_times:
        results_times[benchmark_info] = {}
    if partitions not in results_times[benchmark_info]:
        results_times[benchmark_info][partitions] = []
    results_times[benchmark_info][partitions].append(max(times) - min(times))

f = open("{}/results-times.json".format('./docs'), "w")
f.write(json.dumps(results_times, indent=4, sort_keys=True))
f.close()

f = open("{}/results.json".format(docs_dir), "w")
f.write(json.dumps(results, indent=4, sort_keys=True))
f.close()