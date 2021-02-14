import json
from typing import List

from fastapi import status
from pydantic import parse_obj_as

from crud.crud_article import CRUDArticle
from tests.base import BaseTestCase


class TestArticleAPI(BaseTestCase):
    """ 記事データAPIのテストクラス
    """
    TEST_URL = '/api/v1/articles/'

    def test_一覧取得できること(self):
        # テスト用のデータを作成する
        CRUDArticle(self.db_session).create({'title': 'テストデータ1', 'content': '記事の内容1'})
        CRUDArticle(self.db_session).create({'title': 'テストデータ2', 'content': '記事の内容2'})

        # API実行
        response = self.api_client.get(self.TEST_URL)

        # ステータスコードの検証
        assert response.status_code == status.HTTP_200_OK

        # レスポンスの検証
        response_data = response.json()
        assert len(response_data) == 2
        assert response_data[0]['title'] == 'テストデータ1'
        assert response_data[0]['content'] == '記事の内容1'
        assert response_data[1]['title'] == 'テストデータ2'
        assert response_data[1]['content'] == '記事の内容2'

    def test_記事を登録できること(self):
        data = {'title': '記事登録', 'content': 'テスト用の記事'}

        # API実行
        response = self.api_client.post(
            self.TEST_URL,
            headers={
                'Content-Type': 'application/json'
            },
            json=data)

        # ステータスコードの検証
        assert response.status_code == status.HTTP_200_OK

        # レスポンスの検証
        response_data = response.json()
        assert response_data
        assert response_data['title'] == '記事登録'
        assert response_data['content'] == 'テスト用の記事'
    
    def test_リクエストボディにtitleがない場合は記事の登録に失敗すること(self):
        data = {'content': 'テスト用の記事'}

        # API実行
        response = self.api_client.post(
            self.TEST_URL,
            headers={
                'Content-Type': 'application/json'
            },
            json=data)
        
        # ステータスコードの検証
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

