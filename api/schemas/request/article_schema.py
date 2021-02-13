from api.schemas.request import BaseRequestSchema


class BaseArticleSchema(BaseRequestSchema):
    """ リクエストボディのベース

    title (str): タイトル
    content (str): 本文
    """
    title: str
    content: str


class CreateArticleSchema(BaseArticleSchema):
    """ 記事データ登録用のリクエストボディ
    """
    pass


class UpdateArticleSchema(BaseArticleSchema):
    """ 記事データ更新用のリクエストボディ
    """
    pass
