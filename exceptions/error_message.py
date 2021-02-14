# /usr/bin/env python
# -*- coding: utf-8 -*-


class BaseMessage:
    """ メッセージクラスのベース
    """
    message: str

    def __str__(self) -> str:
        return self.__class__.__name__


class ErrorMessage:
    """ メッセージクラス
    """
    class INTERNAL_SERVER_ERROR(BaseMessage):
        message = 'システムエラーが発生しました、管理者に問い合わせてください'
    
    class INVALID_TOKEN(BaseMessage):
        message = '不正なトークンです'
