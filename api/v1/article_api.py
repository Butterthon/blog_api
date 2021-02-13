# /usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from fastapi import Request

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
