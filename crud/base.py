from typing import Generator, List, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.orm import query, sessionmaker, scoped_session

from core.environment import get_env
from migrations.models.base import Base

ModelType = TypeVar('ModelType', bound=Base)

connection = create_engine(
    get_env().DATABASE_URL,
    echo=get_env().DEBUG,
    encoding='utf-8')


def get_db_session() -> scoped_session:
    """ 新しいDBコネクションを返す

    Returns:
        scoped_session: 新しいDBコネクション
    """
    return scoped_session(sessionmaker(bind=connection))


def generate_db_session() -> Generator[scoped_session, None, None]:
    """ DBコネクションのジェネレータ

    Returns:
        Generator[scoped_session, None, None]: DBコネクションのジェネレータ
    """
    yield get_db_session()


class BaseCRUD:
    """ データアクセスクラスのベース
    """
    model: ModelType = None

    def __init__(
        self,
        db_session: scoped_session,
        include_deleted=False
    ) -> None:
        """ 初期処理

        Args:
            db_session (scoped_session): DBセッション
            include_deleted (bool): 論理削除データも含めるかどうか
        """
        self.db_session = db_session
        self.model.query = self.db_session.query_property()
        self.model.query = self.model.query.execution_options(include_deleted=include_deleted)
    
    def get_query(self) -> query.Query:
        """ ベースクエリ取得

        Returns:
            Query: ベースクエリ
        """
        return self.model.query

    def gets(self) -> List[ModelType]:
        """ 全件取得
        """
        return self.get_query().all()

    def create(self, data: dict = {}) -> ModelType:
        """ 登録

        Args:
            data (dict): 登録データ

        Returns:
            ModelType: 登録後のオブジェクト
        """
        obj = self.model()
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        self.db_session.add(obj)
        self.db_session.flush()
        self.db_session.refresh(obj)
        return obj
