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
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from unicorn.airflow.util.unicorn_airflow_util import load_yaml

dag_id = "unicorn_daily_dag"
dir_path = os.path.dirname(os.path.realpath(__file__))
dag_config = load_yaml(os.path.join(dir_path, dag_id + ".yml"))

default_args = dag_config['default_args']
default_args['start_date'] = datetime.utcnow()

dag = DAG(dag_id,
          default_args=dag_config["default_args"],
          schedule_interval=dag_config["schedule_interval"])

dag.doc_md = dag_config['doc_md']

task1 = BashOperator(task_id='TaskStart',
                     bash_command="echo {{params}}",
                     params={'cmd':dag_config["task1_cmd"]},
                     dag=dag)

task2 = BashOperator(task_id='UnicornDaily',
                     depends_on_past=False,
                     bash_command=dag_config["task1_cmd"],
                     params=dag_config["task1_params"],
                     dag=dag)

task3 = DummyOperator(
    task_id='TaskFinsish',
    dag=dag
)

task2.set_upstream(task1)
task3.set_upstream(task2)



