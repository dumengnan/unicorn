# -*- coding: utf-8 -*-

from __future__ import absolute_import
from datetime import datetime, timedelta


def ds_sub(ds, days):
    ds = datetime.strptime(ds, '%Y-%m-%d')
    if days:
        ds = ds - timedelta(days)
    return ds.isoformat()[:10]
