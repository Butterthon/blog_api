# /usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from fastapi import Request

from api.schemas.request.m_tag_schema import CreateMTagSchema
from crud.crud_m_tag import CRUDMTag
from migrations.models.m_tag import MTag


class MTagAPI:
    """ タグデータに関するAPI
    """
    @classmethod
    def gets(cls, request: Request) -> List[MTag]:
        """ タグデータの一覧取得
        """
        return CRUDMTag(request.state.db_session).gets()

    @classmethod
    def create(cls, request: Request, body: CreateMTagSchema) -> MTag:
        """ タグ登録
        """
        return CRUDMTag(request.state.db_session).create(body.dict())
