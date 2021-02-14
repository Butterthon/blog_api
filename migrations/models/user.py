# /usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import (
    Column,
    func,
    Index,
    INTEGER,
    TEXT,
    text,
    VARCHAR
)

from migrations.models.base import BaseModel


class User(BaseModel):
    """ ユーザー
    """
    __tablename__ = 'users'

    uuid = Column(
        TEXT,
        unique=True,
        server_default=text('gen_random_uuid()'),
        nullable=False,
        comment='画面表示用のID')

    email = Column(
        VARCHAR(254),
        nullable=False,
        comment='メールアドレス')

    username = Column(
        VARCHAR(50),
        nullable=True,
        comment='ユーザー名')

    password = Column(
        VARCHAR(128),
        nullable=False,
        comment='パスワード')
    
    version = Column(
        INTEGER,
        nullable=False,
        default=1,
        comment='バージョン（楽観排他制御用）')

# 論理削除 と 一意性制約を両立させるための部分インデックス
Index('active_unique_email_idx', User.email, unique=True, postgresql_where=(User.deleted_at == None))
