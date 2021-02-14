# /usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import hashlib

from utilities.crypto import CryptoUtils
from utilities.string import StringUtils


class PBKDF2PasswordHasher:
    """ PBKDF2アルゴリズムを使用したパスワードハッシュクラス

    PBKDF2, HMAC, SHA256で構成する

    Attributes:
        algorithm (str): 暗号化アルゴリズム
        digest (_Hash): Hashクラス
    """
    algorithm = 'pbkdf2_sha256'
    digest = hashlib.sha256

    def encode(
        self,
        plain_password: str,
        salt: str,
        iterations: int = 36000
    ) -> str:
        """ 平文のパスワードをハッシュ化する

        Args:
            plain_password (str): 平文のパスワード
            salt (str): ソルト値
            iterations (str): ストレッチングの回数

        Returns:
            str: 平文のパスワードをハッシュ化した文字列

        Raises:
            AssertionError:
                ・平文のパスワードが空文字やNoneが指定された場合
                ・ソルト値に空文字やNoneが指定された、またはソルト値に"$"が含まれてしまっている場合
        """
        assert plain_password is not None
        assert salt and '$' not in salt

        # 平文のパスワード と ソルト値を結合してiterationsの回数分ストレッチング
        hash = CryptoUtils.pbkdf2(
            plain_password,
            salt,
            iterations, self.digest
        )
        hash = base64.b64encode(hash).decode('ascii').strip()

        # 「アルゴリズム名」「ストレッチング回数」「ソルト値」「ハッシュ値」を結合した文字列を返す
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """ 平文のパスワードとハッシュ化されたパスワードを検証する

        Args:
            plain_password (str): 平文のパスワード
            hashed_password (str): ハッシュ化されたパスワード

        Returns:
            bool: 平文のパスワードとハッシュ化されたパスワードのハッシュ値が一致する場合はTrue、一致しない場合はFalse
        """
        _, iterations, salt, _ = hashed_password.split('$', 3)
        encoded_2 = self.encode(plain_password, salt, int(iterations))
        return CryptoUtils.constant_time_compare(hashed_password, encoded_2)


def is_hashed_password_usable(hashed_password: str) -> bool:
    """ ハッシュ化されたパスワードが正当な値かどうか

    Args:
        hashed_password (str): ハッシュ化されたパスワード

    Returns:
        bool: 正当な値であればTrue、それ以外はFalse
    """
    return hashed_password is None or not hashed_password.startswith('!')


def check_password(plain_password: str, hashed_password: str) -> bool:
    """ 平文パスワードがハッシュ化されたパスワードと一致するかどうか

    Args:
        plain_password (str): 平文パスワード
        hashed_password (str): ハッシュ化されたパスワード

    Returns:
        bool: 平文のパスワードとハッシュ化されたパスワードのハッシュ値が一致する場合はTrue、一致しない場合はFalse
    """
    if plain_password is None\
            or not is_hashed_password_usable(hashed_password):
        return False
    return PBKDF2PasswordHasher().verify(plain_password, hashed_password)


def make_password(password: str) -> str:
    """ パスワードをハッシュ化して返す

    Args:
        password (str): パスワード

    Returns:
        str: パスワードをハッシュ化した文字列
    """
    return PBKDF2PasswordHasher()\
        .encode(password, StringUtils.get_random_string())
