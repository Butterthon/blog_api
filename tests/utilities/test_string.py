# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
文字列に関するユーティリティのテストモジュール
"""
from utilities.string import StringUtils


class TestStringUtils(StringUtils):
    """ 文字列に関するユーティリティ「StringUtils」のテストクラス
    """
    def test_get_random_string(self) -> None:
        """ ランダムな文字列生成関数「get_random_string」のテスト
        """
        # 引数に何も指定しない場合、デフォルトの長さの文字列が生成されるかどうか
        no_args_string = self.get_random_string()
        assert len(no_args_string) == 12

        # 長さを指定した場合、指定した長さの文字列が生成されるかどうか
        length = 30
        specified_length_string = self.get_random_string(length=length)
        assert len(specified_length_string) == length
