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

    # # 词 → 编号
    # print("vocab['time']      =", vocab['time'])
    # print("vocab['<pad>']     =", vocab['<pad>'])
    # print("vocab['<unk>']     =", vocab['<unk>'])

    # # 不在词表的词 → 归为 <unk>
    # print("vocab['不存在']     =", vocab['不存在'])

    # # 编号 → 词
    # print('id =', vocab[['time', '<pad>', '<unk>']])
    # print('token =', vocab.to_tokens([2, 0, 1]))


if __name__ == '__main__':
    main()