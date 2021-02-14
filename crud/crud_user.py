from crud.base import BaseCRUD
from migrations.models.user import User


class CRUDMUser(BaseCRUD):
    """ ユーザデータアクセスクラス
    """
    model = User
