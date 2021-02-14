from api.schemas.response import BaseResponseOrmSchema


class UserInDB(BaseResponseOrmSchema):
    """ ユーザデータ

    uuid (str): 主キー
    email (str): メールアドレス
    username (str): ユーザー名
    version (int): バージョン
    """
    uuid: str
    email: str
    username: str
    version: int
