# Airflow
- Concept:
https://airflow.apache.org/concepts.html

## Getting started
- Set Airflow environment
export AIRFLOW_HOME=$PWD/airflow

- Initialize airflow sqlitedb (we don't need it)
airflow initdb

- Start airflow webserver
airflow webserver -p 9090

- Start airflow scheduler
airflow scheduler

https://medium.com/@khatri_chetan/how-to-setup-airflow-multi-node-cluster-with-celery-rabbitmq-cfde7756bb6a

https://github.com/puckel/docker-airflow

```
pip3 install 'apache-airflow[postgres]'
pip3 install 'apache-airflow[celery]'
pip3 install 'apache-airflow[rabbitmq]'
```

- Airflow Tutorial
https://www.youtube.com/watch?v=AHMm1wfGuHE&list=PLYizQ5FvN6pvIOcOd6dFZu3lQqc6zBGp2&index=1

1. Sensors - triggers based off a criteria met
  - waiting for a file to exist in a directory

2. Operators - Execute action
  - pythonoperator
  - branchpythonoperator

3. Transfer - Move files

4. Task Dependencies 
  - ">>, <<"

5. 

# Using Commandline
docker-compose run --rm webserver airflow variable --get var1
docker-compose run --rm webserver airflow variable --set var_old var_new
docker-compose run --rm webserver airflow variable --import /path/to/variable_name_file.json
variable_name_file:
```
{
    "json_key_variable_name": {
        "key1": "value",
        "key2": "value",
    }
}
```