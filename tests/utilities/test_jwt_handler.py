# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
JsonWebTokenの生成や複合に関するユーティリティのテストモジュール
"""
import random
import sys
from calendar import timegm
from datetime import datetime, timedelta

import freezegun
import pytest

from utilities.jwt_handler import (
    jwt_claims_handler,
    jwt_decord_handler,
    jwt_encode_handler,
    jwt_response_handler,
    TYPE_ACCESS_TOKEN,
    TYPE_REFRESH_TOKEN,
)


class DummyUser:
    """ テスト用のダミーユーザー
    """
    def __init__(self):
        self.id = random.randint(1, sys.maxsize)


def test_jwt_claims_handlerの引数token_typeに値を指定しなかった場合はAssertionErrorが発生すること():
    # token_typeが以下の場合、AssertionErrorが発生すること
    # ・指定なし
    # ・空文字
    # ・誤った引数
    with pytest.raises(AssertionError):
        jwt_claims_handler(DummyUser())
    with pytest.raises(AssertionError):
        jwt_claims_handler(DummyUser(), token_type='')
    with pytest.raises(AssertionError):
        jwt_claims_handler(DummyUser(), token_type='acess_token')


@freezegun.freeze_time('2020-01-01')
def test_jwt_claims_handlerで期待したアクセストークン用のクレームセットを生成できること() -> None:
    user = DummyUser()
    claims = jwt_claims_handler(user, token_type=TYPE_ACCESS_TOKEN)

    # クレームセットが辞書型かどうか
    assert isinstance(claims, dict)

    # クレームセットに指定のキーが全て含まれているかどうか
    assert all(
        [key in claims
            for key in ['token_type', 'user_id', 'exp', 'orig_iat']]
    )

    # クレームセットの各値が正しいかどうか
    assert claims['user_id'] == user.id
    assert claims['exp'] == datetime.utcnow() + timedelta(hours=1)
    assert claims['orig_iat'] == timegm(datetime.utcnow().utctimetuple())


@freezegun.freeze_time('2020-01-01')
def test_jwt_claims_handlerで期待したリフレッシュトークン用のクレームセットを生成できること() -> None:
    user = DummyUser()
    claims = jwt_claims_handler(user, token_type=TYPE_REFRESH_TOKEN)

    # クレームセットが辞書型かどうか
    assert isinstance(claims, dict)

    # クレームセットに指定のキーが全て含まれているかどうか
    assert all([key in claims for key in [
            'token_type', 'user_id', 'exp', 'orig_iat']
        ]
    )

    # クレームセットの各値が正しいかどうか
    assert all(
        [
            claims['user_id'] == user.id,
            claims['exp'] == datetime.utcnow() + timedelta(days=90),
            claims['orig_iat'] == timegm(datetime.utcnow().utctimetuple()),
        ]
    )


def test_jwt_encode_handlerがクレームセットのエンコード文字列を返すこと() -> None:
    user = DummyUser()
    claims = jwt_claims_handler(user, token_type=TYPE_ACCESS_TOKEN)
    jwt_string = jwt_encode_handler(claims)

    # 返ってきた値が文字列かどうか
    assert isinstance(jwt_string, str)

    # 返ってきたJWT文字列が空でないかどうか
    assert jwt_string

    # JWT文字列をデコードできるかどうか
    assert isinstance(jwt_decord_handler(jwt_string), dict)


def test_jwt_decord_handlerでJWT文字列をデコードした場合クレームセットが返ってくること() -> None:
    user = DummyUser()
    source_claims = jwt_claims_handler(user, token_type=TYPE_ACCESS_TOKEN)

    jwt_string = jwt_encode_handler(source_claims)
    dest_claims = jwt_decord_handler(jwt_string)

    # デコードして取得したクレームセットが辞書型かどうか
    assert isinstance(dest_claims, dict)

    # 元のクレームセットのデコードして取得したクレームセットが一致するかどうか
    assert source_claims == dest_claims


def test_jwt_response_claims_handler() -> None:
    """ アクセストークンなどを含めたデータを返す「jwt_response_handler」のテスト
    """
    user = DummyUser()

    # キーが"access_token"で、値が上記で生成したアクセストークンの辞書を取得できるかどうか
    claims_by_access_token = jwt_claims_handler(
        user,
        token_type=TYPE_ACCESS_TOKEN
    )
    access_token = jwt_encode_handler(claims_by_access_token)

    # キーが"access_token"で、値が上記で生成したリフレッシュトークンの辞書を取得できるかどうか
    claims_by_refresh_token = jwt_claims_handler(
        user,
        token_type=TYPE_REFRESH_TOKEN
    )
    refresh_token = jwt_encode_handler(claims_by_refresh_token)

    response = jwt_response_handler(access_token, refresh_token)
    assert all(
        [key in response
            for key in ['token_type', TYPE_ACCESS_TOKEN, TYPE_REFRESH_TOKEN]]
    )
