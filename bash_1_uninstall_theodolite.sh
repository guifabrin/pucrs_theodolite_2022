helm uninstall theodolite
kubectl get benchmark | sed 's/|/ /' | awk '{print $1, $8}' | while read line; do kubectl delete benchmark "$line"; done;
kubectl get execution | sed 's/|/ /' | awk '{print $1, $8}' | while read line; do kubectl delete execution "$line"; done;
kubectl get statefulset | sed 's/|/ /' | awk '{print $1, $8}' | while read line; do kubectl delete statefulset "$line"; done;
kubectl get services | sed 's/|/ /' | awk '{print $1, $8}' | while read line; do kubectl delete service "$line"; done;
kubectl get pods | sed 's/|/ /' | awk '{print $1, $8}' | while read line; do kubectl delete pod "$line" ; done;

# CRDs for Theodolite
kubectl delete crd executions.theodolite.com
kubectl delete crd benchmarks.theodolite.com
# CRDs for Prometheus operator (see https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack#uninstall-chart)
kubectl delete crd alertmanagerconfigs.monitoring.coreos.com
kubectl delete crd alertmanagers.monitoring.coreos.com
kubectl delete crd podmonitors.monitoring.coreos.com
kubectl delete crd probes.monitoring.coreos.com
kubectl delete crd prometheuses.monitoring.coreos.com
kubectl delete crd prometheusrules.monitoring.coreos.com
kubectl delete crd servicemonitors.monitoring.coreos.com
kubectl delete crd thanosrulers.monitoring.coreos.com


kubectl delete crd kafkas.kafka.strimzi.io
kubectl delete crd kafkaconnects.kafka.strimzi.io
kubectl delete crd strimzipodsets.core.strimzi.io
kubectl delete crd kafkatopics.kafka.strimzi.io
kubectl delete crd kafkausers.kafka.strimzi.io
kubectl delete crd kafkamirrormakers.kafka.strimzi.io
kubectl delete crd kafkabridges.kafka.strimzi.io
kubectl delete crd kafkaconnectors.kafka.strimzi.io
kubectl delete crd kafkamirrormaker2s.kafka.strimzi.io
kubectl delete crd kafkarebalances.kafka.strimzi.io