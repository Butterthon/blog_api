# /usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import APIRouter
from api.endpoints.v1.article import article_api_router
from api.endpoints.v1.m_tag import m_tag_api_router
from api.endpoints.v1.user import user_api_router

v1_api_router = APIRouter()

# 記事データAPI
v1_api_router.include_router(
    article_api_router,
    prefix='/articles',
    tags=['articles'])

# タグデータAPI
v1_api_router.include_router(
    m_tag_api_router,
    prefix='/tags',
    tags=['tags'])

# ユーザデータAPI
v1_api_router.include_router(
    user_api_router,
    prefix='/users',
    tags=['users'])
