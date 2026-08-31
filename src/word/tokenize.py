lines = [
    'the time machine by h g wells',
    'twinkled and his usually pale face was flushed',
    'the time traveller proceeded',
    'any real body must have extension in four directions',
    'but some of you will say',
    'there are three dimensions',
    'four if we count time',
    'scientific people have very little patience',
    'they say to the student',
    'you blame a man for so small a difference',
    'and yet it is not so small',
]


def tokenize(lines, token='word'):  #@save
    """将文本行拆分为单词或字符词元"""
    if token == 'word':
        return [line.split() for line in lines]
    elif token == 'char':
        return [list(line) for line in lines]
    else:
        print('错误：未知词元类型：' + token)



tokens = tokenize(lines, token='word')
for i in range(11):
    print(tokens[i])



