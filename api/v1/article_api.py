# /usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from fastapi import Request

from api.schemas.request.article_schema import CreateArticleSchema
from crud.crud_article import CRUDArticle
from migrations.models.article import Article


class ArticleAPI:
    """ 記事データに関するAPI
    """
    @classmethod
    def gets(cls, request: Request) -> List[Article]:
        """ 記事データの一覧取得
        """
        return CRUDArticle(request.state.db_session).gets()

    @classmethod
    def create(cls, request: Request, body: CreateArticleSchema) -> Article:
        """ 記事投稿
        """
        return CRUDArticle(request.state.db_session).create(body.dict())
