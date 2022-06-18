# python3 py_3_generate_benchmarks_and_executions.py

for file in "benchmarks/*.yaml"; do kubectl apply -f "./${file}"; done;

for file in "executions/*.yaml"; do kubectl apply -f "./${file}"; done;

./bash_3_delete_finished.sh