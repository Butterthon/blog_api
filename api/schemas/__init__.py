# /usr/bin/env python
# -*- coding: utf-8 -*-
import re


def to_camel(string: str):
    """ スネークケースをキャメルケースに変換
    """
    return re.sub('_(.)', lambda s: s.group(1).upper(), string)
