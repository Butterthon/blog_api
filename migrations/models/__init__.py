# /usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import os

IGNORE_FILE_NAMES = ['__init__.py', '__pycache__']
MODEL_FILES = os.listdir(os.path.dirname(__file__))
[
    importlib.import_module(
        f'migrations.models.{model_file.replace(".py", "")}',
    )
    for model_file in MODEL_FILES
    if model_file not in IGNORE_FILE_NAMES
]
