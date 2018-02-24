# -*- coding: utf-8 -*-

import yaml


def load_yaml(file_name):
    f = open(file_name)
    yaml_data = yaml.load(f)
    f.close()
    return yaml_data