# /usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

import pydantic

from api.schemas import to_camel


class BaseResponseOrmSchema(pydantic.BaseModel):
    """ レスポンススキーマのベース

    created_at (datetime): 登録日時
    updated_at (datetime): 最終更新日時
    deleted_at (datetime): 削除日時
    """
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
