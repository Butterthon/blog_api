# /usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Depends, Request

from api.schemas.request.article_schema import CreateArticleSchema
from api.schemas.response.article_schema import ArticleInDB
from api.v1.article_api import ArticleAPI
from dependencies import set_db_session_in_request
from migrations.models.article import Article

article_api_router = APIRouter()

@article_api_router.get(
    '/',
    response_model=List[ArticleInDB],
    dependencies=[Depends(set_db_session_in_request)])
async def gets(request: Request) -> List[Article]:
    """ 記事データを全件取得
    """
    return ArticleAPI.gets(request)


@article_api_router.post(
    '/',
    response_model=ArticleInDB,
    dependencies=[Depends(set_db_session_in_request)])
async def create(request: Request, body: CreateArticleSchema) -> Article:
    """ 記事投稿
    """
    return ArticleAPI.create(request, body)
