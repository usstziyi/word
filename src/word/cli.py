from word.vocabulary import Vocab
from word.tokenize import tokenize


def main():

    with open('src/book/input.txt', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    # 分词：原始文本 → 二维词列表
    tokens = tokenize(lines, token='word')

    # 建词表：二维词列表 → 词序号映射表
    vocab = Vocab(tokens)

    print('词表大小:', len(vocab))

    # 词 → 编号
    print("vocab['time']      =", vocab['time'])  # → Vocab.__getitem__(vocab, 'time')        → 返回编号
    print("vocab['<pad>']     =", vocab['<pad>'])  # → Vocab.__getitem__(vocab, '<pad>')       → 返回 0
    print("vocab['<unk>']     =", vocab['<unk>'])  # → Vocab.__getitem__(vocab, '<unk>')       → 返回 1

    # 不在词表的词 → 归为 <unk>
    print("vocab['不存在']     =", vocab['不存在'])

    # 编号 → 词
    print('id =', vocab[['time', '<pad>', '<unk>']]) # → Vocab.__getitem__(vocab, ['time', '<pad>', '<unk>'])
    print('token =', vocab.to_tokens([2, 0, 1])) # → Vocab.to_tokens(vocab, [2, 0, 1])

    # 保存词表到文件
    vocab.save('src/word/vocab.txt')
    print('词表已保存到 src/word/vocab.txt')

    # 从文件加载词表，验证编号一致
    loaded = Vocab.load('src/word/vocab.txt')
    print('加载后的词表大小:', len(loaded))
    print("loaded['time']      =", loaded['time'])
    print('loaded.to_tokens([2, 0, 1]) =', loaded.to_tokens([2, 0, 1]))


if __name__ == '__main__':
    main()