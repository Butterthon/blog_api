from api.schemas.request import BaseRequestSchema


class BaseMTagSchema(BaseRequestSchema):
    """ リクエストボディのベース

    name (str): タグ名称
    """
    name: str


class CreateMTagSchema(BaseMTagSchema):
    """ 記事データ登録用のリクエストボディ
    """
    pass


class UpdateMTagSchema(BaseMTagSchema):
    """ 記事データ更新用のリクエストボディ
    """
    pass
