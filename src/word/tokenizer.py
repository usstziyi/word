"""分词器：把文本按词或按字符切分成 token。"""


def tokenizer(lines: list[str], token: str = 'word') -> list[list[str]]:
    """把每一行文本切分成 token 列表。

    Args:
        lines: 原始文本行列表，每行一个字符串。
        token: 切分粒度，``'word'`` 按空白切词，``'char'`` 按字符切分。

    Returns:
        二维列表，外层对应行，内层是每行的 token 列表。

    Raises:
        ValueError: 当 ``token`` 不是 ``'word'`` 或 ``'char'`` 时。
    """
    if token == 'word':
        return [line.split() for line in lines]
    elif token == 'char':
        return [list(line) for line in lines]
    else:
        raise ValueError(f'错误：未知词元类型：{token!r}')