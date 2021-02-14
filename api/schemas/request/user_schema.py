from pydantic import EmailStr, Field, validator

from api.schemas.request import BaseRequestSchema
from migrations.models.user import User

MAX_LENGTH_PASSWORD = User.password.property.columns[0].type.length


class BaseUserSchema(BaseRequestSchema):
    """ リクエストボディのベース

    email (EmailStr): メールアドレス
    username (str): ユーザ名
    """
    email: EmailStr
    username: str = Field(..., max_length=50)


class CreateUserSchema(BaseUserSchema):
    """ ユーザ情報登録用のリクエストボディ

    password (str): パスワード
    confirm_password (str): パスワード（確認用）
    """
    password: str = Field(..., max_length=128)
    confirm_password: str = Field(..., max_length=128)


class UpdateUserSchema(BaseUserSchema):
    """ ユーザ情報更新用のリクエストボディ
    """
    """ ユーザ情報登録用のリクエストボディ

    password (str): パスワード
    confirm_password (str): パスワード（確認用）
    """
    password: str = Field(None, max_length=128)
    confirm_password: str = Field(None, max_length=128)
