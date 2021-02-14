import psycopg2
from sqlalchemy_utils import database_exists, drop_database
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from core.environment import get_env
from migrations.models.base import Base
# from sqlalchemy.orm import scoped_session, sessionmaker
from tests.db_session import test_connection

# conftestで初期データを登録する場合はこのSessionを使用する
# Session = scoped_session(
#     sessionmaker(
#         bind=test_connection
#     )
# )


def create_test_database():
    # テストDBが削除されずに残ってしまっている場合は削除
    if database_exists(get_env().TEST_DATABASE_URL):
        drop_database(get_env().TEST_DATABASE_URL)

    # テストDB作成
    coonection = psycopg2.connect('host=db user=postgres password=postgres')
    coonection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = coonection.cursor()
    cursor.execute(f'CREATE DATABASE {get_env().TEST_DATABASE_URL.split("/")[-1]}')

    # テストDBにコネクション追加
    coonection = psycopg2.connect(f'host=db dbname={get_env().TEST_DATABASE_URL.split("/")[-1]} user=postgres password=postgres')
    coonection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = coonection.cursor()
    cursor.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto')

    # テストDBにテーブル追加
    Base.metadata.create_all(bind=test_connection)


def pytest_sessionstart(session):
    """ pytest実行時に一度だけ呼ばれる処理
    """
    # テストDB作成
    create_test_database()


def pytest_sessionfinish(session, exitstatus):
    """ pytest終了時に一度だけ呼ばれる処理
    """
    # テストDB削除
    if database_exists(get_env().TEST_DATABASE_URL):
        drop_database(get_env().TEST_DATABASE_URL)
