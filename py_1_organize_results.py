from os import listdir, rename
from os.path import isfile, join
import json

from numpy import partition

temp_dir = './temp'
results_dir = './results'
docs_dir = './docs'
exp_actual = 0

try:
    f = open("{}/expID.txt".format(results_dir), "r")
    exp_actual = int(f.read())+1
    f.close()
except:
    pass

total_exp = 0
try:
    f = open("{}/expID.txt".format(temp_dir), "r")
    total_exp = int(f.read())
    f.close()
except:
    pass
for experiment_id in range(0, total_exp + 1):
    try:
        files = [f for f in listdir('{}'.format(temp_dir)) if isfile(join(temp_dir, f)) and ('exp{}_'.format(experiment_id) in f or 'exp{}-'.format(experiment_id) in f)]
        for file in files:
            actual_file = '{}/{}'.format(temp_dir, file)
            new_file = '{}/{}'.format(results_dir, file.replace('exp{}_'.format(experiment_id), 'exp{}_'.format(exp_actual)).replace('exp{}-'.format(experiment_id), 'exp{}-'.format(exp_actual)))
            rename(actual_file, new_file)
        f = open("{}/expID.txt".format(results_dir), "w")
        f.write(str(exp_actual))
        f.close()
        exp_actual+=1
    except:
        pass
        
results = {}
for experiment_id in range(0, exp_actual):
    try:
        f = open("{}/exp{}-execution-configuration".format(results_dir, experiment_id), "r")
        execution_configuration = json.loads(f.read())
        f.close()
        f = open("{}/exp{}_demand.csv".format(results_dir, experiment_id), "r")
        demand = f.readlines()
        f.close()
        benchmark_info = execution_configuration['benchmark'].replace('-1600','').replace('-160','').replace('-400','')
        partitions = 40
        try:
            partitions = int(execution_configuration['benchmark'].split('-')[-1])
        except:
            pass
        if benchmark_info not in results:
            results[benchmark_info] = {}
        if str(partitions) not in results[benchmark_info]:
            results[benchmark_info][str(partitions)] = {}
        for line in demand:
            if 'load,resources' in line:
                continue
            values = line.strip().split(',')
            if len(values) < 2 or values[1]=='-2147483648':
                continue
            if str(values[0]) not in results[benchmark_info][str(partitions)]:
                results[benchmark_info][str(partitions)][values[0]] = []
            results[benchmark_info][str(partitions)][values[0]].append(int(values[1]))
    except:
        pass

f = open("{}/results.json".format(docs_dir), "w")
f.write(json.dumps(results, indent=4, sort_keys=True))
f.close()