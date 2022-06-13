import re
import os

deployments = {
  'flink':['taskmanager'],
  'beam-flink':['taskmanager']
}

for uc in ['uc1', 'uc2', 'uc3']:
  for stream in ['kstreams', 'beam-flink', 'beam-samza', 'flink']:
    for slo in ['generic', 'lag trend', 'lag trend ratio', 'dropped records', 'dropped records ratio']:
      for search in ['FullSearch', 'LinearSearch', 'BinarySearch']:
          search_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', search).lower().replace(' ','-')
          slo_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', slo).lower().replace(' ','-')
          if stream not in deployments:
            deployments[stream] = ['{0}-{1}'.format(uc, stream)]
          for deployment_resource in deployments[stream]:
            deployment_resource_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', deployment_resource).lower().replace(' ','-')
            filename = "executions/{0}-{1}-{2}-{3}-{4}-execution.yaml".format(uc, stream, slo_snake_case, search_snake_case, deployment_resource_snake_case)
            if os.path.exists(filename): continue
            file = open(filename, "a")
            file.write("""apiVersion: theodolite.com/v1
kind: execution
metadata:
  name: {0}-{1}-{7}-{5}-{6}
spec:
  benchmark: "{0}-{1}"
  load:
    loadType: "NumSensors"
    loadValues: [25000, 50000, 75000, 100000, 125000, 150000]
  resources:
    resourceType: "Instances"
    resourceValues: [1, 2]
  slos:
    - sloType: "{2}"
      prometheusUrl: "http://prometheus-operated:9090"
      offset: 0
      properties:
        threshold: 2000
        externalSloUrl: "http://localhost:80/evaluate-slope"
        warmup: 60 # in seconds
  execution:
    strategy: "{3}"
    duration: 300 # in seconds
    repetitions: 1
    loadGenerationDelay: 30 # in seconds
    restrictions:
      - "LowerBound"
  configOverrides:
    - patcher:
        type: "SchedulerNamePatcher"
        resource: "{4}-deployment.yaml"
      value: "random-scheduler" """.format(uc, stream, slo, search, deployment_resource, search_snake_case, deployment_resource_snake_case, slo_snake_case))
            file.close()

for stream in ['kstreams', 'beam-flink', 'beam-samza', 'flink']:
    for uc in ['uc4']:
      for slo in ['generic', 'lag trend', 'lag trend ratio', 'dropped records', 'dropped records ratio']:
        for search in ['FullSearch', 'LinearSearch', 'BinarySearch']:
            search_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', search).lower().replace(' ','-')
            slo_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', slo).lower().replace(' ','-')
            if stream not in deployments:
              deployments[stream] = ['{0}-{1}'.format(uc, stream)]
            for deployment_resource in deployments[stream]:
              deployment_resource_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', deployment_resource).lower().replace(' ','-')
              filename = "executions/{0}-{1}-{2}-{3}-{4}-execution.yaml".format(uc, stream, slo_snake_case, search_snake_case, deployment_resource_snake_case)
              if os.path.exists(filename): continue
              file = open(filename, "a")
              file.write("""apiVersion: theodolite.com/v1
kind: execution
metadata:
  name: {0}-{1}-{7}-{5}-{6}
spec:
  benchmark: "{0}-{1}"
  load:
    loadType: "NumNestedGroups"
    loadValues: [25000, 50000, 75000, 100000, 125000, 150000]
  resources:
    resourceType: "Instances"
    resourceValues: [1, 2]
  slos:
    - sloType: "{1}"
      prometheusUrl: "http://prometheus-operated:9090"
      offset: 0
      properties:
        threshold: 2000
        externalSloUrl: "http://localhost:80/evaluate-slope"
        warmup: 60 # in seconds
  execution:
    strategy: "{3}"
    duration: 300 # in seconds
    repetitions: 1
    loadGenerationDelay: 30 # in seconds
    restrictions:
      - "LowerBound"
  configOverrides:
    - patcher:
        type: "SchedulerNamePatcher"
        resource: "{4}-deployment.yaml"
      value: "random-scheduler" """.format(uc, stream, slo, search, deployment_resource, search_snake_case, deployment_resource_snake_case, slo_snake_case))
              file.close()