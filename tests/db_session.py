from threading import local as thread_local

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from core.environment import get_env

_thread_local = thread_local()

test_connection = create_engine(
    get_env().TEST_DATABASE_URL,
    encoding='utf8',
    pool_pre_ping=True)


def set_test_db_session(db_session: scoped_session) -> None:
    """ スレッドローカルにテスト用のDBセッションをセット
    """
    setattr(_thread_local, 'db_session', db_session)


def get_test_db_session() -> scoped_session:
    """ スレッドローカルからテスト用のDBセッションを取得
    """
    return getattr(_thread_local, 'db_session')


class TestingSession(Session):
    """ テスト実行時だけcommit()の挙動を変える必要があるため、Sessionクラスをオーバライド
    """
    def commit(self):
        self.flush()
        self.expire_all()


class TestingScopedSession(scoped_session):
    """ HTTPミドルウェアのremove()で何も実行されないよう、scoped_sessionをオーバライド
    """
    def remove(self):
        pass  # 何もしない

    def test_remove(self):
        """ テスト実行時のremove関数
        """
        if self.registry.has():
            self.registry().close()
        self.registry.clear()


def get_test_db_session() -> TestingScopedSession:
    """ テスト用のDBセッションを返す
    """
    return TestingScopedSession(
        sessionmaker(
            bind=test_connection,
            class_=TestingSession,
            expire_on_commit=False
        )
    )
