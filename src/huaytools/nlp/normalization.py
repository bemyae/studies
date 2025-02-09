#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-08-17 7:36 下午

Author:
    huayang

Subject:

"""
import re
import doctest
import unicodedata

from typing import Callable

try:
    import opencc

    t2s = opencc.OpenCC('t2s.json').convert
except:  # noqa
    t2s = lambda s: s

RE_MULTI_SPACE = re.compile(r'\s+', re.U)
RE_NUMERIC = re.compile(r'[-+]?((\d+\.?\d*)|(\d*\.?\d+))([eE][-+]?\d+)?')

# 一些特殊处理的全角到半角映射
FULL2HALF_SPECIAL = {
    '\u3000': ' ',  # 全角空格
    '。': '.',  # 中文句号
}


def is_whitespace(char):
    """Checks whether `char` is a whitespace character.

    Examples:
        >>> is_whitespace(' ')
        True
        >>> is_whitespace(chr(12288))  # 全角空格
        True
    """
    # \t, \n, and \r are technically control characters but we treat them
    # as whitespace since they are generally considered as such.
    if char == ' ' or char == '\t' or char == '\n' or char == '\r':
        return True
    cat = unicodedata.category(char)
    if cat == 'Zs':
        return True
    return False


def is_control(char):
    """
    Checks whether `char` is a control character.

    Examples:
        >>> is_control(chr(9))  # tab；注意：在 doctest 里面不能直接使用 is_char_control('\t')
        False
        >>> is_control(chr(8))  # 退格
        True
    """
    # These are technically control characters but we count them as whitespace characters.
    if char == '\t' or char == '\n' or char == '\r':
        return False
    cat = unicodedata.category(char)
    if cat.startswith('C'):  # transformers
        return True
    return False


def is_punctuation(char):
    """Checks whether `char` is a punctuation character.

    Examples:
        >>> is_punctuation(',')
        True
        >>> is_punctuation('+')
        True
        >>> is_punctuation('@')
        True
        >>> is_punctuation('^')
        True
    """
    cp = ord(char)
    # We treat all non-letter/number ASCII as punctuation.
    # Characters such as "^", "$", and "`" are not in the Unicode
    # Punctuation class but we treat them as punctuation anyways, for
    # consistency.
    if (33 <= cp <= 47) or (58 <= cp <= 64) or (91 <= cp <= 96) or (123 <= cp <= 126):
        return True
    cat = unicodedata.category(char)
    if cat.startswith('P'):
        return True
    return False


def is_end_of_word(text):
    """Checks whether the last character in text is one of a punctuation, control or whitespace character.

    References: transformers.tokenization_utils
    """
    last_char = text[-1]
    return bool(is_control(last_char) | is_punctuation(last_char) | is_whitespace(last_char))


def is_start_of_word(text):
    """Checks whether the first character in text is one of a punctuation, control or whitespace character."""
    first_char = text[0]
    return bool(is_control(first_char) | is_punctuation(first_char) | is_whitespace(first_char))


def convert_to_unicode(text):
    """Converts `text` to Unicode (if it's not already), assuming utf-8 input."""
    if isinstance(text, str):
        return text
    elif isinstance(text, bytes):
        return text.decode("utf-8", "ignore")
    else:
        raise ValueError("Unsupported string type: %s" % (type(text)))


def convert_to_simplified(s):
    """繁转简

    Examples:
        >>> convert_to_simplified('我愛python')
        '我爱python'
    """
    return t2s(s)


def is_full_alphabet(c):
    """是否全角字母"""
    if isinstance(c, str):
        c = ord(c)
    return (0xFF21 <= c <= 0xFF3A) or (0xFF41 <= c <= 0xFF5A)


def is_full_number(c):
    """是否全角数字"""
    if isinstance(c, str):
        c = ord(c)
    return 0xFF10 <= c <= 0xFF19


def is_half(char):
    """是否半角字符

    Examples:
        >>> is_half(',')
        True
        >>> is_half('。')
        False
    """
    if isinstance(char, str):
        char = ord(char)
    return 0x0020 <= char <= 0x007E


def is_full(char):
    """是否全角字符

    Examples：
        >>> is_full('。')
        True
        >>> is_full(',')
        False
    """
    if isinstance(char, int):
        try:
            char = chr(char)
        except:
            return False
    return is_half(ord(char) - 0xFEE0) or char in FULL2HALF_SPECIAL


def is_chinese(char):
    """是否中文字符

    Examples:
        >>> is_chinese('我')
        True
        >>> is_chinese('の')
        False
    """
    if isinstance(char, str):
        char = ord(char)
    return 0x4E00 <= char <= 0x9FA5


def is_cjk(char):
    """Checks whether CP is the codepoint of a CJK(Chinese, Japanese, Korean) character.

    Examples:
        >>> is_cjk('我')
        True
        >>> is_cjk('1')
        False
    """
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all of the other languages.

    if isinstance(char, str):
        char = ord(char)

    if ((0x4E00 <= char <= 0x9FFF) or
            (0x3400 <= char <= 0x4DBF) or
            (0x20000 <= char <= 0x2A6DF) or
            (0x2A700 <= char <= 0x2B73F) or
            (0x2B740 <= char <= 0x2B81F) or
            (0x2B820 <= char <= 0x2CEAF) or
            (0xF900 <= char <= 0xFAFF) or
            (0x2F800 <= char <= 0x2FA1F)):
        return True

    return False


def is_numeric(string):
    """
    Examples:
        >>> is_numeric('12.3')
        True
        >>> is_numeric('+1.2e-3')
        True
        >>> is_numeric('.3')
        True
        >>> is_numeric('3.')
        True
        >>> is_numeric('.3e-3')
        True
        >>> is_numeric('1.2.3')
        False
        >>> is_numeric('.3e')
        False

    """
    # try:
    #     float(s)
    #     return True
    # except:
    #     return False
    if RE_NUMERIC.fullmatch(string):
        return True
    return False


def full2half(c):
    """全角转半角

    Examples:
        >>> full2half('，')
        ','
        >>> full2half('。')
        '.'
        >>> full2half('是')
        '是'
    """
    if c in FULL2HALF_SPECIAL:
        return FULL2HALF_SPECIAL.get(c)
    else:
        i = ord(c) - 0xFEE0
        return chr(i) if is_half(i) else c  # 转完之后不是半角字符返回原来的字符


def normalize(s: str, r=' ',
              to_lower=True,
              to_simplified=True,
              _remove_accents=True,
              _remove_numeric=False,
              _remove_punctuation=False):
    """

    Examples:
        >>> _s = '我試試……你看看你。。我愛 Python，How are You！有串数字(+1.2e-3)'
        >>> normalize(_s, _remove_numeric=True, _remove_punctuation=True)
        '我试试 你看看你 我爱 python how are you 有串数字'

    Args:
        s:
        r:
        to_lower:
        to_simplified: 繁转简
        _remove_accents:
        _remove_punctuation:
        _remove_numeric:
    """

    if to_lower:
        s = s.lower()

    if to_simplified:
        s = convert_to_simplified(s)

    if _remove_accents:
        s = remove_accents(s)

    # should before `remove_punctuation`
    if _remove_numeric:
        s = remove_numeric(s, r)

    if _remove_punctuation:
        s = remove_punctuation(s, r)

    s = remove_multi_space(s, r)
    return s.strip()


def remove_multi_space(s, r=' '):
    """ 替换连续空格为一个空格

    Examples:
        >>> remove_multi_space('a   b  c')
        'a b c'
    """
    return RE_MULTI_SPACE.sub(r, s)


def remove_accents(s):
    """remove accents from a piece of text.

    Examples:
        >>> _s = 'âbĉ'
        >>> remove_accents(_s)
        'abc'
    """
    s = unicodedata.normalize('NFD', s)
    output = []
    for c in s:
        if unicodedata.category(c) == 'Mn':
            continue
        output.append(c)
    return ''.join(output)


def remove_numeric(s, r=' '):
    """
    移除数字

    Examples:
        >>> remove_numeric('测试[12,12.,1.2,0.12,.12,+0.12,-0.12,-.12,+.12,1E2,+1.2e-2]')
        '测试[ , , , , , , , , , , ]'

    Args:
        s:
        r:
    """
    return RE_NUMERIC.sub(r, s)


def remove_punctuation(s, r=' '):
    """ 移除标点符号，并用 `r` 代替

    Examples:
        >>> _s = '我试试，你看看。'
        >>> remove_punctuation(_s)
        '我试试 你看看 '
    """
    ret = []
    for c in s:
        if is_punctuation(c):
            ret.append(r)
        else:
            ret.append(c)
    return ''.join(ret)


def strip_by(judge_fn: Callable):
    """
    根据 `judge_fn` 移除一段文本头尾符号

    Examples:
        >>> jfn = lambda c: c.isnumeric()
        >>> strip_by(jfn)('1测试1')  # 移除两侧的数字，因为 jfn('1') 为 True，所以会被移除
        '测试'
        >>> strip_by(is_punctuation)(',测试.')  # 移除两侧的标点
        '测试'
    """

    def strip_fn(s):
        start = 0
        for start, c in enumerate(s):
            if not judge_fn(c):
                break

        end = 0
        for end, c in enumerate(s[::-1]):
            if not judge_fn(c):
                break

        end = len(s) - end

        return s[start: end]

    return strip_fn


def _test():
    doctest.testmod()


if __name__ == "__main__":
    _test()
