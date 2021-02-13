from crud.base import BaseCRUD
from migrations.models.article import Article


class CRUDArticle(BaseCRUD):
    """ 記事データアクセスクラス
    """
    model = Article
