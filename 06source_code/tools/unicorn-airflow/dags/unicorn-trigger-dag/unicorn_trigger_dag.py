# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from unicorn.airflow.util.unicorn_airflow_util import load_yaml
from airflow.utils.trigger_rule import TriggerRule


dag_id = "unicorn_trigger_dag"
dir_path = os.path.dirname(os.path.realpath(__file__))
dag_config = load_yaml(os.path.join(dir_path, dag_id + ".yml"))

default_args = dag_config['default_args']
default_args['start_date'] = datetime.utcnow()

dag = DAG(dag_id,
         default_args=dag_config["default_args"],
         schedule_interval=dag_config["schedule_interval"])

dag.doc_md = dag_config['doc_md']


def run_this_func(ds, **kwargs):
    print("Remotely received value of {} for key=message".format(kwargs['dag_run'].conf['message']))


task1 = PythonOperator(
    task_id='TaskStart',
    provide_context=True,
    python_callable=run_this_func,
    dag=dag)

task2 = BashOperator(task_id='CrawlFollower',
                     depends_on_past=False,
                     bash_command=dag_config["task2_cmd"],
                     params=dag_config["task_params"],
                     dag=dag)

task3 = BashOperator(task_id='CrawlFriends',
                     depends_on_past=False,
                     bash_command=dag_config["task3_cmd"],
                     params=dag_config["task_params"],
                     dag=dag)

task4 = BashOperator(task_id='GetAllScreenName',
                     depends_on_past=False,
                     bash_command=dag_config["task4_cmd"],
                     params=dag_config["task_params"],
                     dag=dag)

task5 = BashOperator(task_id='CrawlContent',
                     depends_on_past=False,
                     bash_command=dag_config["task5_cmd"],
                     params=dag_config["task_params"],
                     dag=dag)

task6 = DummyOperator(
    task_id='TaskFinsish',
    dag=dag,
    trigger_rule=TriggerRule.ALL_DONE
)

task2.set_upstream([task1])
task3.set_upstream([task1])
task4.set_upstream([task2, task3])
task5.set_upstream([task4])
task6.set_upstream([task5])

