# -*- coding: utf-8 -*-

from unicorn.airflow.plugins.unicorn_macros import ds_sub
from airflow.plugins_manager import AirflowPlugin


class UnicornPlugin(AirflowPlugin):
    name = "UnicornPlugin"
    macros = [
        ds_sub
    ]
