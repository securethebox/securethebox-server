from controllers.elasticsearch_controller import ElasticSearch
import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
import pendulum

local_tz = pendulum.timezone("America/Los_Angeles")

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(0),
}

dag = DAG(
    dag_id='my_first_dag',
    default_args=args,
    schedule_interval=None,
    catchup=False,
)

existingIpAddressesList = ['30.156.16.163', '164.85.94.243', '50.184.59.162', '236.212.255.77', '16.241.165.21', '246.106.125.113']

def getAllIpAddresses(**context):
    date = context['execution_date']
    newdate = local_tz.convert(date)
    print(newdate.strftime("%Y-%m-%d"))
    print(newdate)
    return newdate

t1 = PythonOperator(
    task_id='get_all_ip_addresses',
    python_callable=getAllIpAddresses,
    provide_context=True,
    dag=dag
)

t4 = DummyOperator(
    task_id='join',
    trigger_rule='one_success',
    provide_context=True,
    dag=dag
)

t1 >> t4
