# /usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base, declared_attr, DeclarativeMeta
from sqlalchemy.sql.functions import current_timestamp
from sqla_softdelete import SoftDeleteMixin

Base: DeclarativeMeta = declarative_base()


class BaseModel(Base, SoftDeleteMixin):
    """ ベースモデル

    Attibutes:
        id (INTEGER): 主キー
        created_at (TIMESTAMP): 登録日時
        updated_at (TIMESTAMP): 最終更新日時
        deleted_at (TIMESTAMP): 最終削除日時（SoftDeleteMixinクラスが持っている属性）
    """
    __abstract__ = True

    id = Column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )

    created_at = Column(
        'created_at',
        TIMESTAMP(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
        comment='登録日時',
    )

    updated_at = Column(
        'updated_at',
        TIMESTAMP(timezone=True),
        onupdate=current_timestamp(),
        comment='最終更新日時',
    )

    @declared_attr
    def __mapper_args__(cls) -> Dict[str, str]:
        """ デフォルトのソート順は主キーの昇順
        """
        return {'order_by': 'id'}
