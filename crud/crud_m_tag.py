from crud.base import BaseCRUD
from migrations.models.m_tag import MTag


class CRUDMTag(BaseCRUD):
    """ タグデータアクセスクラス
    """
    model = MTag
