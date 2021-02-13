from api.schemas.response import BaseResponseOrmSchema


class MTagInDB(BaseResponseOrmSchema):
    """ 記事データ

    id (int): 主キー
    name (str): タグの名称
    """
    id: int
    name: str
