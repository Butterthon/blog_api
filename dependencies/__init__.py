from fastapi import Depends, Request
from sqlalchemy.orm import scoped_session

from crud.base import generate_db_session


async def set_db_session_in_request(
    request: Request,
    db_session: scoped_session = Depends(generate_db_session)
) -> None:
    """ リクエストにDBセッションをセットする
    """
    request.state.db_session = db_session
