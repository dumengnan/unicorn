# -*- coding: utf-8 -*-

import unittest as unittest
from unicorn.airflow.plugins.unicorn_macros import ds_sub


class UnicornMacrosTest(unittest.TestCase):
    def test_ds_sub(self):
        day = ds_sub("2018-02-28", 1)
        self.assertEqual("2018-02-27", day)
