from os import listdir
from os.path import isfile, join
import json

results_dir = './results'
docs_dir = './docs'

def get_total_experiments(directory = results_dir):
    experiment = 0
    try:
        f = open("{}/expID.txt".format(directory), "r")
        experiment = int(f.read())+1
        f.close()
    except:
        pass
    return experiment

def get_experiment_files(experiment_id, directory = results_dir):
    return [f for f in listdir('{}'.format(directory)) if isfile(join(directory, f)) and ('exp{}_'.format(experiment_id) in f or 'exp{}-'.format(experiment_id) in f)]

def get_experiment_configuration(experiment_id, directory = results_dir):
    f = open("{}/exp{}-execution-configuration".format(directory, experiment_id), "r")
    execution_configuration = json.loads(f.read())
    f.close()
    return execution_configuration

def get_experiment_demand(experiment_id, directory = results_dir):
    demand = []
    try:
        f = open("{}/exp{}_demand.csv".format(directory, experiment_id), "r")
        demand = f.readlines()
        f.close()
    except:
        pass
    return demand

def get_experiment_benchmark(experiment_id, directory = results_dir):
    partitions = 40
    benchmark_info = None
    try:
        execution_configuration = get_experiment_configuration(experiment_id, directory)
        benchmark_info = execution_configuration['benchmark'].replace('-1600','').replace('-160','').replace('-400','')
        try:
            partitions = int(execution_configuration['benchmark'].split('-')[-1])
        except:
            pass
    except:
        pass
    return benchmark_info, str(partitions)