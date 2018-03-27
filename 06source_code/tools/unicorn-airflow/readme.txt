Trigger APi Demo:
curl -d '{"conf":"{\"input\":\"/opt/crawler_data/id.txt\"}"}' http://192.168.0.6:8090/api/experimental/dags/unicorn_trigger_dag/dag_runs -X POST