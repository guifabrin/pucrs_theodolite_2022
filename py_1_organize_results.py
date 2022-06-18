from os import listdir, rename
from os.path import isfile, join
import json

from numpy import partition

results_dir = './docs'
exp_actual = 0

try:
    f = open("{}/organized/expID.txt".format(results_dir), "r")
    exp_actual = int(f.read())+1
    f.close()
except:
    pass

folders = [f for f in listdir(results_dir) if not isfile(join(results_dir, f)) and f != 'organized' ]
for folder in folders:
    total_exp = 0
    try:
        f = open("{}/{}/expID.txt".format(results_dir,folder), "r")
        total_exp = int(f.read())
        f.close()
    except:
        pass
    for experiment_id in range(0, total_exp + 1):
        try:
            files = [f for f in listdir('{}/{}'.format(results_dir, folder)) if isfile(join(results_dir, folder, f)) and ('exp{}_'.format(experiment_id) in f or 'exp{}-'.format(experiment_id) in f)]
            for file in files:
                actual_file = '{}/{}/{}'.format(results_dir, folder, file)
                new_file = '{}/organized/{}'.format(results_dir, file.replace('exp{}_'.format(experiment_id), 'exp{}_'.format(exp_actual)).replace('exp{}-'.format(experiment_id), 'exp{}-'.format(exp_actual)))
                rename(actual_file, new_file)
            f = open("{}/organized/expID.txt".format(results_dir), "w")
            f.write(str(exp_actual))
            f.close()
            exp_actual+=1
        except:
            pass
        
results = {}
for experiment_id in range(0, exp_actual):
    try:
        f = open("{}/organized/exp{}-execution-configuration".format(results_dir, experiment_id), "r")
        execution_configuration = json.loads(f.read())
        f.close()
        f = open("{}/organized/exp{}_demand.csv".format(results_dir, experiment_id), "r")
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

f = open("{}/results.json".format(results_dir), "w")
f.write(json.dumps(results, indent=4, sort_keys=True))
f.close()

csv_file = ['benchmark;system;size;40;160;400;1600']
for key in results:
    uc = key.split('-')[0]
    for size in ['10000','20000','4000','8000','16000','32000','64000','128000','256000','512000','1024000','2048000']: 
        r_40 = ''
        try:
            r_40 = str(sum(results[key]['40'][size])/len(results[key]['40'][size])).replace('.',',')
        except:
            pass
        r_160 = ''
        try:
            r_160 = str(sum(results[key]['160'][size])/len(results[key]['160'][size])).replace('.',',')
        except:
            pass
        r_400 = ''
        try:
            r_400 = str(sum(results[key]['400'][size])/len(results[key]['400'][size])).replace('.',',')
        except:
            pass
        r_1600 = ''
        try:
            r_1600 = str(sum(results[key]['1600'][size])/len(results[key]['1600'][size])).replace('.',',')
        except:
            pass
        line = ';'.join([uc, key.replace('{}-'.format(uc), ''), size, r_40, r_160, r_400, r_1600])
        csv_file.append(line)

f = open("{}/results.csv".format(results_dir), "w")
f.write('\n'.join(csv_file))
f.close()
