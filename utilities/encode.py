# /usr/bin/env python
# -*- coding: utf-8 -*-


class EncodingUtils:
    """ エンコーディングのユーティリティ
    """
    @classmethod
    def force_bytes(
        cls,
        s,
        encoding: str = 'utf-8',
        errors: str = 'strict',
    ) -> bytes:
        """ 引数encodingで指定されたエンコーディングルール通りに変換したバイトデータを返す

        Args:
            s: エンコーディングしたい文字列
            errors (str): エンコーディングルールに従った変換ができなかった場合の対応方法、デフォルトは'strict'（UnicodeDecodeErrorをスローする）

        Returns:
            bytes:  エンコーディングされたバイトデータ
        """
        # 引数sがバイトデータの場合
        if isinstance(s, bytes):
            # 引数encodingがutf-8の場合、sをそのまま返す
            if encoding == 'utf-8':
                return s

            # 上記以外は、引数sを指定のエンコーディングルール通りに変換したバイトデータを返す
            else:
                return s.decode('utf-8', errors).encode(encoding, errors)
        return str(s).encode(encoding, errors)
