# /usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Depends, Request

from api.schemas.request.m_tag_schema import CreateMTagSchema
from api.schemas.response.m_tag_schema import MTagInDB
from api.v1.m_tag_api import MTagAPI
from dependencies import set_db_session_in_request
from migrations.models.m_tag import MTag

m_tag_api_router = APIRouter()

@m_tag_api_router.get(
    '/',
    response_model=List[MTagInDB],
    dependencies=[Depends(set_db_session_in_request)])
async def gets(request: Request) -> List[MTag]:
    """ タグデータを全件取得
    """
    return MTagAPI.gets(request)

@m_tag_api_router.post(
    '/',
    response_model=MTagInDB,
    dependencies=[Depends(set_db_session_in_request)])
async def create(request: Request, body: CreateMTagSchema) -> MTag:
    """ タグ登録
    """
    return MTagAPI.create(request, body)
