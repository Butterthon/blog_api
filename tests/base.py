# /usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient

from crud.base import generate_db_session
from main import app
from tests.db_session import get_test_db_session, set_test_db_session


class BaseTestCase:
    """ テストクラスのベース
    """
    def setup_method(self, method) -> None:
        """ 前処理
        """
        self.db_session = get_test_db_session()

        # スレッドローカルにDBセッションをセット
        set_test_db_session(self.db_session)

        # APIクライアントの設定
        self.api_client = TestClient(app, base_url='https://localhost')

        # アプリが使用するDBをテスト用のものに切り替える
        app.dependency_overrides[generate_db_session] = self.override_generate_db_session
    
    def teardown_method(self, method) -> None:
        """ 後処理
        """
        # ロールバック
        self.db_session.test_remove()

        # オーバーライドしたDBを元に戻す
        app.dependency_overrides[self.override_generate_db_session] = generate_db_session

    def override_generate_db_session(self):
        """ DBセッションの依存性オーバーライド関数
        """
        yield self.db_session
