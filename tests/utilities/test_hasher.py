# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
パスワードハッシュに関するユーティリティのテストモジュール
"""
from utilities.hasher import (
    check_password,
    is_hashed_password_usable,
    make_password,
    PBKDF2PasswordHasher,
)


def test_make_passwordでハッシュ化したパスワードと元のパスワードが一致すること() -> None:
    plain_password = 'password'
    hashed_password = make_password(plain_password)
    assert plain_password != hashed_password
    assert check_password(plain_password, hashed_password)


def test_make_passwordでハッシュ化したパスワードが元のパスワード以外の文字列と一致しないこと() -> None:
    plain_password = 'password'
    hashed_password = make_password(plain_password)
    assert plain_password != hashed_password
    assert not check_password('', hashed_password)
    assert not check_password('p@ssword', hashed_password)
    assert not check_password('passw0rd', hashed_password)
    assert not check_password('passwOrd', hashed_password)
    assert not check_password('Password', hashed_password)
    assert not check_password('pasSword', hashed_password)


def test_make_passwordでハッシュ化したパスワードの形式が正しいこと() -> None:
    plain_password = 'password'
    hashed_password = make_password(plain_password)
    assert is_hashed_password_usable(hashed_password)
    assert hashed_password.startswith(PBKDF2PasswordHasher.algorithm)
