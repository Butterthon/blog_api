# /usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from fastapi import Request

from api.mixins import ApiMixin
from api.schemas.request.user_schema import CreateUserSchema
from crud.crud_user import CRUDMUser
from migrations.models.user import User


class UserAPI(ApiMixin):
    """ ユーザデータに関するAPI
    """
    @classmethod
    def gets(cls, request: Request) -> List[User]:
        """ ユーザデータの一覧取得
        """
        return CRUDMUser(request.state.db_session).gets()

    @classmethod
    def create(cls, request: Request, body: CreateUserSchema) -> User:
        """ ユーザ登録
        """
        return CRUDMUser(request.state.db_session).create(body.dict())
