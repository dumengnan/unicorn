#!/usr/bin/python
# -*- coding: utf-8 -*-
# THIS FILE IS MANAGED BY THE GLOBAL REQUIREMENTS REPO - DO NOT EDIT
import setuptools

# In python < 2.7.4, a lazy loading of package `pbr` will break
# setuptools if some other modules registered functions in `atexit`.
# solution from: http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing  # noqa
except ImportError:
    pass

setuptools.setup(    
    name='unicorn-airflow',
    description='Programmatically author, schedule and monitor data pipelines',
    author='mee'
)