python3 run_3_execution.py

kubectl get execution | sed 's/|/ /' | awk '{print $1, $8}' | while read line; do kubectl delete execution "$line"; done;

for file in "executions/*.yaml"; do kubectl apply -f "./${file}"; done;