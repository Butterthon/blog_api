# /usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import hmac
from typing import Any

from utilities.encode import EncodingUtils


class CryptoUtils:
    """ 暗号化/複合化のユーティリティ
    """
    @classmethod
    def pbkdf2(
        cls,
        plain_password: str,
        salt: str,
        iterations: int,
        digest: Any,
        dklen: int = 0,
    ) -> str:
        """ PBKDF2アルゴリズムを使用して平文のパスワードをハッシュ化して返す

        Args:
            plain_password (str): 平文のパスワード
            salt (str): ソルト値
            iterations (int): ストレッチングの回数
            digest (Any): ハッシュ関数
            dklen (int): 生成鍵長(オクテット)

        Returns:
            str: パスワードをハッシュ化した文字列
        """
        dklen = dklen or None
        plain_password = EncodingUtils.force_bytes(plain_password)
        salt = EncodingUtils.force_bytes(salt)
        return hashlib.pbkdf2_hmac(
            digest().name, plain_password, salt, iterations, dklen
        )

    @classmethod
    def constant_time_compare(cls, value1: str, value2: str) -> bool:
        """ 2つの文字列（value1 と value2）が等しいかどうか

        Args:
            value1 (str): 文字列1
            value2 (str): 文字列2

        Returns:
            bool: 文字列が等しい場合はTrue, 等しくない場合はFalse
        """
        return hmac.compare_digest(
            EncodingUtils.force_bytes(value1),
            EncodingUtils.force_bytes(value2)
        )
