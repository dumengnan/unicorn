# -*- coding: utf-8 -*-

import unicorn_macros
from airflow.plugins_manager import AirflowPlugin


class UnicornPlugin(AirflowPlugin):
    name = "UnicornPlugin"
    macros = [
        unicorn_macros.ds_sub
    ]
