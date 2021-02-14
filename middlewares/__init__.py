# /usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from starlette.middleware import authentication
from starlette.middleware.base import BaseHTTPMiddleware

from core.environment import get_env
from crud.base import get_db_session
from exceptions import ApiException, SystemException
from exceptions.error_message import ErrorMessage
from tests.db_session import get_test_db_session
from utilities.jwt_handler import (
    jwt_decord_handler,
    TYPE_ACCESS_TOKEN,
    TYPE_REFRESH_TOKEN
)


class ProcessRequestMiddleware(BaseHTTPMiddleware):
    """ HTTPリクエスト/レスポンス用ミドルウェア
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        """ ミドルウェアの処理

        Args:
            request (Request): リクエスト情報
            call_next (method): 次の処理

        Returns:
            Response: レスポンス
        """
        # リクエストにDBセッション追加
        # swagger-UI表示時にrequest.stateにdb_sessionがなくて怒られてしまう件の対策
        if not getattr(request.state, 'db_session', False):
            request.state.db_session = get_db_session()

        # pytest実行時はスレッドローカルからdb_sessionを取得してセット
        if getattr(get_env(), 'is_test', False):
            request.state.db_session = get_test_db_session()

        try:
            response = await call_next(request)

        # アプリケーション例外発生時
        except ApiException as ae:
            return JSONResponse(ae.detail, status_code=ae.status_code)

        # リクエストボディ例外発生時
        except RequestValidationError as rve:
            errors = jsonable_encoder(rve.errors())
            return JSONResponse(
                {'detail': errors},
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # システム例外発生時
        except Exception as e:
            e = SystemException(e)
            return JSONResponse(e.detail, status_code=e.status_code)

        # 正常終了時はトランザクションコミット
        else:
            request.state.db_session.commit()
            return response

        finally:
            # DBセッション破棄
            request.state.db_session.remove()


class AuthenticationBackend(authentication.AuthenticationBackend):
    """ 認証ミドルウェアのバックエンド
    """
    async def authenticate(self, request: Request):
        """ 認証処理

        Args:
            request (Request): リクエスト情報
        """
        request.state.user_id = None

        # リクエストにDBセッション追加(例外発生時のエラー対策)
        request.state.db_session = get_db_session() if not getattr(get_env(), 'is_test', False) else get_test_db_session()

        authorization: str = request.headers.get('Authorization')
        scheme, access_token = get_authorization_scheme_param(authorization)

        # リクエストヘッダに認証情報が無い場合は何もしない
        if not authorization or scheme.lower() != 'bearer':
            return

        # JWTをデコードしてクレームセットを取得
        try:
            claims = jwt_decord_handler(access_token)

        # トークンタイプ不一致など
        except ApiException as ae:
            raise ae

        # アクセストークン期限切れ
        except jwt.ExpiredSignatureError:
            raise ApiException(
                create_error(ErrorMessage.EXPIRED_TOKEN),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        # その他エラーの場合は何もしない
        except Exception as e:
            return

        # クレームセットのユーザーIDをリクエスト情報にセット
        request.state.user_id = claims['user_id']
