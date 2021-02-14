# /usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import (
    Column,
    INTEGER,
    TEXT,
    text,
)

from migrations.models.base import BaseModel


class Article(BaseModel):
    """ ブログ記事
    """
    __tablename__ = 'articles'

    uuid = Column(
        TEXT,
        unique=True,
        server_default=text('gen_random_uuid()'),
        nullable=False,
        index=True,
        comment='画面表示用のID')

    title = Column(
        TEXT,
        nullable=False,
        comment='タイトル')
    
    content = Column(
        TEXT,
        nullable=False,
        comment='記事本文')

    version = Column(
        INTEGER,
        nullable=False,
        default=1,
        comment='バージョン（楽観排他制御用）')
