import os
import re

deployments = {
    'flink': ['taskmanager'],
    'beam-flink': ['taskmanager']
}

slos = {
    'lag trend': {
        'externalSloUrl': "\"http://localhost:80/evaluate-slope\"",
        'threshold': 1000,
        'warmup': '0',
    },
    'lag trend ratio': {
        'externalSloUrl': "\"http://localhost:80/evaluate-slope\"",
        'ratio': 1,
        'warmup': '0',
    },
    'generic': {
        'externalSloUrl': "\"http://localhost:80/evaluate-slope\"",
        'queryAggregation': 'max',
        'repetitionAggregation': 'median',
        'operator': 'lte',
        'threshold': '1000',
        'promQLQuery': '\"sum by(job) (kafka_streams_stream_task_metrics_dropped_records_total>=0)\"'
    },
    'dropped records': {
        'externalSloUrl': "\"http://localhost:80/evaluate-slope\"",
        'threshold': 1000,
        'warmup': '0',
    },
    'dropped records ratio': {
        'externalSloUrl': "\"http://localhost:80/evaluate-slope\"",
        'ratio': 1,
        'warmup': '0',
    }
}
for partitions in ['', '-160', '-400', '-1600']:
    for uc in ['uc1', 'uc2', 'uc3']:
        for stream in ['kstreams', 'beam-flink', 'beam-samza', 'flink']:
            for slo in ['lag trend']:
                slo_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', slo).lower().replace(' ', '-')
                for search in ['BinarySearch']:
                    search_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', search).lower().replace(' ', '-')
                    if stream not in deployments:
                        deployments[stream] = ['{0}-{1}'.format(uc, stream)]
                    for deployment_resource in deployments[stream]:
                        deployment_resource_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-',
                                                                deployment_resource).lower().replace(' ', '-')
                        filename = "executions/{0}-{1}-{2}-{3}-{4}{5}-execution.yaml".format(uc, stream, slo_snake_case,
                                                                                             search_snake_case,
                                                                                             deployment_resource_snake_case,
                                                                                             partitions)
                        file = open(filename, "w")
                        properties = ''
                        for key in slos[slo]:
                            properties += '\n        {0}: {1}'.format(key, slos[slo][key])
                        file.write("""apiVersion: theodolite.com/v1
kind: execution
metadata:
  name: {0}-{1}-{7}-{5}-{6}{9}
spec:
  benchmark: "{0}-{1}{9}"
  load:
    loadType: "NumSensors"
    loadValues: [10000, 20000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 512000, 1024000, 2048000]
  resources:
    resourceType: "Instances"
    resourceValues: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  slos:
    - sloType: "{2}"
      prometheusUrl: "http://prometheus-operated:9090"
      offset: 0
      properties: {8}
  execution:
    strategy: "{3}"
    duration: 60 # in seconds
    repetitions: 1
    loadGenerationDelay: 0 # in seconds
    restrictions: []
  configOverrides: [] """.format(uc,
                                 stream,
                                 slo,
                                 search,
                                 deployment_resource,
                                 search_snake_case,
                                 deployment_resource_snake_case,
                                 slo_snake_case,
                                 properties, partitions))
                        file.close()
for partitions in ['', '-160', '-400']:
    for stream in ['kstreams', 'beam-flink', 'beam-samza', 'flink']:
        for uc in ['uc4']:
            for slo in ['lag trend']:
                search_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', search).lower().replace(' ', '-')
                for search in ['BinarySearch']:
                    slo_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-', slo).lower().replace(' ', '-')
                    if stream not in deployments:
                        deployments[stream] = ['{0}-{1}'.format(uc, stream)]
                    for deployment_resource in deployments[stream]:
                        deployment_resource_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '-',
                                                                deployment_resource).lower().replace(' ', '-')
                        filename = "executions/{0}-{1}-{2}-{3}-{4}{5}-execution.yaml".format(uc, stream, slo_snake_case,
                                                                                             search_snake_case,
                                                                                             deployment_resource_snake_case,
                                                                                             partitions)
                        file = open(filename, "w")
                        properties = ''
                        for key in slos[slo]:
                            properties += '\n        {0}: {1}'.format(key, slos[slo][key])
                        file.write("""apiVersion: theodolite.com/v1
kind: execution
metadata:
  name: {0}-{1}-{7}-{5}-{6}{9}
spec:
  benchmark: "{0}-{1}{9}"
  load:
    loadType: "NumNestedGroups"
    loadValues: [1, 2, 3, 4, 5, 6, 7, 8, 9]
  resources:
    resourceType: "Instances"
    resourceValues: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  slos:
    - sloType: "{2}"
      prometheusUrl: "http://prometheus-operated:9090"
      offset: 0
      properties: {8}
  execution:
    strategy: "{3}"
    duration: 60 # in seconds
    repetitions: 1
    loadGenerationDelay: 0 # in seconds
    restrictions: []
  configOverrides: []""".format(
                            uc,
                            stream,
                            slo,
                            search,
                            deployment_resource,
                            search_snake_case,
                            deployment_resource_snake_case,
                            slo_snake_case,
                            properties,
                            partitions
                        ))
                        file.close()
