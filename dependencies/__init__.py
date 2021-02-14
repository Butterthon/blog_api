from fastapi import Depends, Request
from sqlalchemy.orm import scoped_session

from crud.base import generate_db_session
from exceptions.error_message import ErrorMessage
from utilities.auth import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')

async def login_required(
    request: Request,
    token: str = Depends(oauth2_scheme),
) -> None:
    """ ユーザーがログインしているかどうか
    """
    """ ユーザーがログインしているかどうか

    Args:
        request (Request): リクエスト情報
        token (str): アクセストークン

    Raises:
        ApiException: ログインしていない場合はAPI例外をスローする
    """
    if not request.state.user_id:
        raise ApiException(
            create_error(ErrorMessage.INVALID_TOKEN),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


async def set_db_session_in_request(
    request: Request,
    db_session: scoped_session = Depends(generate_db_session)
) -> None:
    """ リクエストにDBセッションをセットする
    """
    request.state.db_session = db_session
