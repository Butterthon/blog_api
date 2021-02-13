from api.schemas.response import BaseResponseOrmSchema


class ArticleInDB(BaseResponseOrmSchema):
    """ 記事データ

    title (str): タイトル
    content (str): 本文
    """
    title: str
    content: str
