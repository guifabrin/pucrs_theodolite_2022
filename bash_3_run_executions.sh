for file in "benchmarks/*.yaml"; do kubectl apply -f "./${file}"; done;

for file in "executions/*.yaml"; do kubectl apply -f "./${file}"; done;