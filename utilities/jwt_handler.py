# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
このモジュールはJsonWebTokenの生成や複合に関するユーティリティ提供する
"""
from calendar import timegm
from datetime import datetime, timedelta
from typing import Any, Dict

from jose import jwt

from core.environment import get_env
from migrations.models.user import User

TYPE_ACCESS_TOKEN = 'access_token'
TYPE_REFRESH_TOKEN = 'refresh_token'
TYPE_RESET_PASSWORD = 'reset_password'

PROTECTED_TOKEN_TYPES = (
    TYPE_ACCESS_TOKEN,
    TYPE_REFRESH_TOKEN,
    TYPE_RESET_PASSWORD
)


def jwt_claims_handler(user: User, token_type: str = '') -> Dict[str, Any]:
    """ クレームセットを生成

    Args:
        user (User): クレームセット含めるユーザー情報
        token_type (str): トークンタイプ

    Returns:
        Dict[str, Any]: クレームセット

    Raises:
        AssertionError: 不正なトークンタイプが指定された場合
    """
    assert token_type in PROTECTED_TOKEN_TYPES, \
        f'引数token_type には{"、または".join(PROTECTED_TOKEN_TYPES)}を指定してください'

    claims = {
        'token_type': token_type,
        'user_id': user.id,
        'orig_iat': timegm(datetime.utcnow().utctimetuple()),
    }

    # 「アクセストークン」の有効期限設定
    if claims['token_type'] == TYPE_ACCESS_TOKEN:
        claims['exp'] = datetime.utcnow() + timedelta(seconds=get_env().JWT_ACCESS_TOKEN_EXPIRE)

    # 「リフレッシュトークン」の有効期限設定
    elif claims['token_type'] == TYPE_REFRESH_TOKEN:
        claims['exp'] = datetime.utcnow() + timedelta(seconds=get_env().JWT_REFRESH_TOKEN_EXPIRE)

    # 「パスワード再設定用ワンタイムトークン」の有効期限設定
    elif claims['token_type'] == TYPE_RESET_PASSWORD:
        claims['exp'] = datetime.utcnow() + timedelta(seconds=get_env().JWT_ONE_TIME_TOKEN_EXPIRE)
    return claims


def jwt_encode_handler(claims: dict) -> str:
    """ クレームセットをエンコードしてJWT文字列を返す

    Args:
        claims (dict): クレームセット

    Returns:
        str: JsonWebToken
    """
    return jwt.encode(
        claims,
        get_env().JWT_SECRET_KEY,
        get_env().JWT_ALGORITHM
    )


def jwt_decord_handler(jwt_string: str) -> Dict[str, Any]:
    """ JWT文字列をデコードしてクレームセットを返す

    Args:
        jwt_string (str): JWT文字列

    Returns:
        Dict[str, Any]: JWTをデコードして取得したクレームセット
    """
    claims = jwt.decode(
        jwt_string,
        get_env().JWT_SECRET_KEY,
        algorithms=get_env().JWT_ALGORITHM,)
    return claims


def jwt_response_handler(
    access_token: str,
    refresh_token: str,
) -> Dict[str, str]:
    """ JWT文字列を含んだ辞書データを返す

    Args:
        access_token (str): アクセストークン
        refresh_token (str): リフレッシュトークン

    Returns:
        Dict[str, str]: JWT認証レスポンス
    """
    return {
        'token_type': 'bearer',
        TYPE_ACCESS_TOKEN: access_token,
        TYPE_REFRESH_TOKEN: refresh_token,
    }
