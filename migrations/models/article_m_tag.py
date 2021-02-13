# /usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, INTEGER, TEXT

from migrations.models.base import BaseModel
from migrations.models.article import Article
from migrations.models.m_tag import MTag


class ArticleMTag(BaseModel):
    """ ブログ記事 と タグの中間テーブル
    """
    __tablename__ = 'article_m_tags'

    article_id = Column(INTEGER, ForeignKey(f'{Article.__tablename__}.id'))
    m_tag_id = Column(INTEGER, ForeignKey(f'{MTag.__tablename__}.id'))
