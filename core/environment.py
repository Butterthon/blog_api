# /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from functools import lru_cache

from pydantic import BaseSettings

PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Environment(BaseSettings):
    """ 環境変数を扱うクラス
    """
    DEBUG: bool
    DATABASE_URL: str

    class Config:
        env_file = os.path.join(PROJECT_ROOT_DIR, '.env')


@lru_cache
def get_env():
    """ .envの読み取り結果をキャッシュ
    """
    return Environment()
