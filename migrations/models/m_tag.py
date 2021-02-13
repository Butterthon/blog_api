# /usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, TEXT

from migrations.models.base import BaseModel


class MTag(BaseModel):
    """ ブログ記事に付与するタグ
    """
    __tablename__ = 'm_tags'

    name = Column(
        TEXT,
        nullable=False,
        comment='記事に付与するタグの名称')
