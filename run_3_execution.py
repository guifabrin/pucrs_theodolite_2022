import re
import os

deployments = {
  'flink':['taskmanager'],
  'beam-flink':['taskmanager']
}

slos = {
  'lag trend': {
     'externalSloUrl': "\"http://localhost:80/evaluate-slope\"" ,
     'threshold': 1000,
     'warmup': '60',
  },
  'lag trend ratio':{
     'externalSloUrl':"\"http://localhost:80/evaluate-slope\"" ,
     'ratio': 1,
     'warmup': '60',
  },
  'generic': {
     'externalSloUrl': "\"http://localhost:80/evaluate-slope\"" ,
     'queryAggregation': 'max',
    'repetitionAggregation': 'median',
    'operator': 'lte',
    'threshold': '1000',
    'promQLQuery': '\"sum by(job) (kafka_streams_stream_task_metrics_dropped_records_total>=0)\"'
  },
  'dropped records':{
     'externalSloUrl': "\"http://localhost:80/evaluate-slope\"" ,
     'threshold': 1000,
     'warmup': '60',
  },
  'dropped records ratio':{
     'externalSloUrl':"\"http://localhost:80/evaluate-slope\"" ,
     'ratio': 1,
     'warmup': '60',
  }
}

for uc in ['uc1', 'uc2', 'uc3']:
  for stream in ['kstreams', 'beam-flink', 'beam-samza', 'flink', 'hazelcastjet']:
    for slo in ['lag trend', 'lag trend ratio', 'generic', 'dropped records', 'dropped records ratio']:
      for search in ['FullSearch', 'LinearSearch', 'BinarySearch']:
          search_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', search).lower().replace(' ','-')
          slo_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', slo).lower().replace(' ','-')
          if stream not in deployments:
            deployments[stream] = ['{0}-{1}'.format(uc, stream)]
          for deployment_resource in deployments[stream]:
            deployment_resource_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', deployment_resource).lower().replace(' ','-')
            filename = "executions/{0}-{1}-{2}-{3}-{4}-execution.yaml".format(uc, stream, slo_snake_case, search_snake_case, deployment_resource_snake_case)
            file = open(filename, "w")
            properties = ''
            for key in slos[slo]:
              properties+='\n        {0}: {1}'.format(key, slos[slo][key])
            file.write("""apiVersion: theodolite.com/v1
kind: execution
metadata:
  name: {0}-{1}-{7}-{5}-{6}
spec:
  benchmark: "{0}-{1}"
  load:
    loadType: "NumSensors"
    loadValues: [25000, 50000]
  resources:
    resourceType: "Instances"
    resourceValues: [1, 2, 3, 4, 5, 6]
  slos:
    - sloType: "{2}"
      prometheusUrl: "http://prometheus-operated:9090"
      offset: 0
      properties: {8}
  execution:
    strategy: "{3}"
    duration: 120 # in seconds
    repetitions: 1
    loadGenerationDelay: 30 # in seconds
    restrictions:
      - "LowerBound"
  configOverrides:
    - patcher:
        type: "SchedulerNamePatcher"
        resource: "{4}-deployment.yaml"
      value: "random-scheduler" """.format(uc, stream, slo, search, deployment_resource, search_snake_case, deployment_resource_snake_case, slo_snake_case, properties))
            file.close()

for stream in ['kstreams', 'beam-flink', 'beam-samza', 'flink', 'hazelcastjet']:
    for uc in ['uc4']:
      for slo in ['lag trend', 'lag trend ratio', 'generic', 'dropped records', 'dropped records ratio']:
        for search in ['FullSearch', 'LinearSearch', 'BinarySearch']:
          search_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', search).lower().replace(' ','-')
          slo_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', slo).lower().replace(' ','-')
          if stream not in deployments:
            deployments[stream] = ['{0}-{1}'.format(uc, stream)]
          for deployment_resource in deployments[stream]:
            deployment_resource_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', deployment_resource).lower().replace(' ','-')
            filename = "executions/{0}-{1}-{2}-{3}-{4}-execution.yaml".format(uc, stream, slo_snake_case, search_snake_case, deployment_resource_snake_case)
            file = open(filename, "w")
            properties = ''
            for key in slos[slo]:
              properties+='\n        {0}: {1}'.format(key, slos[slo][key])
            file.write("""apiVersion: theodolite.com/v1
kind: execution
metadata:
  name: {0}-{1}-{7}-{5}-{6}
spec:
  benchmark: "{0}-{1}"
  load:
    loadType: "NumNestedGroups"
    loadValues: [25000, 50000]
  resources:
    resourceType: "Instances"
    resourceValues: [1, 2, 3, 4, 5, 6]
  slos:
    - sloType: "{1}"
      prometheusUrl: "http://prometheus-operated:9090"
      offset: 0
      properties: {8}
  execution:
    strategy: "{3}"
    duration: 120 # in seconds
    repetitions: 1
    loadGenerationDelay: 30 # in seconds
    restrictions:
      - "LowerBound"
  configOverrides:
    - patcher:
        type: "SchedulerNamePatcher"
        resource: "{4}-deployment.yaml"
      value: "random-scheduler" """.format(uc, stream, slo, search, deployment_resource, search_snake_case, deployment_resource_snake_case, slo_snake_case, properties))
            file.close()