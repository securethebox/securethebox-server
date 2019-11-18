import time
from builtins import range
from pprint import pprint

import airflow
from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(
    dag_id='my_first_dag',
    default_args=args,
    schedule_interval=None,
)


# [START howto_operator_python]
def print_context(ds, **kwargs):
    pprint(kwargs)
    print(ds)
    return 'Whatever you return gets printed in the logs'


# This is a task set as a variable
run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag,
)
# [END howto_operator_python]


# [START howto_operator_python_kwargs]
def my_sleeping_function(random_base):
    """This is a function that will run within the DAG execution"""
    time.sleep(random_base)


# Generate 5 sleeping tasks, sleeping from 0.0 to 0.4 seconds respectively
for i in range(5):
    task = PythonOperator(
        task_id='sleep_for_' + str(i),
        python_callable=my_sleeping_function,
        op_kwargs={'random_base': float(i) / 10},
        dag=dag,
    )

    # task depends on run_this to be completed before running
    run_this >> task

    # a << b = Depends on b to complete before running a
    # a >> [b,c] = after a, run b and c in parallel
    # 

# Getting Variables:
# In Airflow Admin>Variables, variable_name_in_airflow = {"key1","value", "key2", "value"}
# some_variable = Variable.get("variable_name_in_airflow", deserialize_json = True)
# var1 = some_variable["key1"]
# var2 = some_variable["key2"]