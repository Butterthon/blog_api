# /usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Depends, Request

from api.schemas.request.user_schema import CreateUserSchema
from api.schemas.response.user_schema import UserInDB
from api.v1.user_api import UserAPI
from dependencies import login_required, set_db_session_in_request
from migrations.models.user import User

user_api_router = APIRouter()

@user_api_router.get(
    '/',
    response_model=List[UserInDB],
    dependencies=[
        Depends(set_db_session_in_request),
        Depends(login_required)])
async def gets(request: Request) -> List[User]:
    """ ユーザデータを全件取得
    """
    return UserAPI.gets(request)

@user_api_router.post(
    '/',
    response_model=UserInDB,
    dependencies=[
        Depends(set_db_session_in_request),
        Depends(login_required)])
async def create(request: Request, body: CreateUserSchema) -> User:
    """ ユーザ登録
    """
    return UserAPI.create(request, body)
