#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml


def get_config():
    with open('etc/config.yml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg