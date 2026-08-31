def tokenize(lines, token='word'):  #@save
    """将文本行拆分为单词或字符词元

    参数:
        lines: 文本行列表，如 ['the time machine', ...]
        token: 词元类型，'word' 按单词拆分，'char' 按字符拆分

    返回:
        list[list[str]]: 二维列表，每个元素是该行拆分后的词元列表

    异常:
        ValueError: 传入未知的 token 类型
    """
    if token == 'word':
        return [line.split() for line in lines]
    elif token == 'char':
        return [list(line) for line in lines]
    else:
        raise ValueError(f'错误：未知词元类型：{token!r}')

