# /usr/bin/env python
# -*- coding: utf-8 -*-
import pydantic

from api.schemas import to_camel


class BaseRequestSchema(pydantic.BaseModel):
    """ リクエストスキーマのベース
    """
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
