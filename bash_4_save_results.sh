while true
do
    clear
    mkdir -p ./docs/temp/
    kubectl get executions
    kubectl cp $(kubectl get pod -l app=theodolite -o jsonpath="{.items[0].metadata.name}"):results ./docs/temp/ -c results-access
    python py_4_process_results_demand.py
    sleep 30
done