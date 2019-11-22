from controllers.elasticsearch_controller import ElasticSearch
import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(
    dag_id='my_first_dag',
    default_args=args,
    schedule_interval=None,
)

existingIpAddressesList = ['30.156.16.163', '164.85.94.243', '50.184.59.162', '236.212.255.77', '16.241.165.21', '246.106.125.113']

def getAllIpAddresses():
    es = ElasticSearch()
    es.setIndex("kibana_sample_data_logs")
    return list(es.queryIPAddresses())
    
def printIpAddress(ip):
    print(ip)

def addIpAddress(ip):
    existingIpAddressesList.append(ip)

def printAllExistingIps():
    return len(existingIpAddressesList)

def check_if_ip_exists_in_list(**kwargs):
    if kwargs['ip'] in existingIpAddressesList:
        return "print_ip"
    else:
        return "add_ip"

allIP = getAllIpAddresses()

# This is a task set as a variable
t1 = PythonOperator(
    task_id='get_all_ip_addresses',
    python_callable=getAllIpAddresses,
    dag=dag
)

t4 = PythonOperator(
    task_id='join',
    python_callable=printAllExistingIps,
    trigger_rule='one_success',
    dag=dag
)

b1 = BranchPythonOperator(
        task_id='branching',
        python_callable=lambda: getAllIpAddresses,
        dag=dag,
    )

t1 >> b1 

for x in allIP:

    t = DummyOperator(
        task_id=x,
        dag=dag,
    )

    t2 = PythonOperator(
        task_id='print_ip',
        python_callable=printIpAddress,
        op_kwargs={'ip': x},
        dag=dag
    )
    
    t3 = PythonOperator(
        task_id='add_ip',
        python_callable=addIpAddress,
        op_kwargs={'ip': x},
        dag=dag
    )

    c1 = BranchPythonOperator(
        task_id='follow_' + x,
        provide_context=True,
        python_callable=check_if_ip_exists_in_list,
        dag=dag,
    )

    b1 >> t >> [t2,t3] >> t4




if __name__ == "__main__":
    my_sleeping_function("test")