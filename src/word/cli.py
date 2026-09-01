"""演示脚本：分词 → 建词表 → 查表 → 保存/加载词表。"""

from word.tokenizer import tokenizer
from word.vocabulary import Vocab


def main() -> None:
    """运行完整流程演示。"""

    with open('src/book/input.txt', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    # 分词：text → tokens
    tokens = tokenizer(lines, token='word')

    # 建词表：tokens -> indices
    vocab = Vocab(tokens)

    print('词表大小:', len(vocab))

    # 词 → 编号
    print("vocab['time']      =", vocab['time'])  # → Vocab.__getitem__(vocab, 'time')        → 返回编号
    print("vocab['<pad>']     =", vocab['<pad>'])  # → Vocab.__getitem__(vocab, '<pad>')       → 返回 0
    print("vocab['<unk>']     =", vocab['<unk>'])  # → Vocab.__getitem__(vocab, '<unk>')       → 返回 1

    # 不在词表的词 → 归为 <unk>
    print("vocab['不存在']     =", vocab['不存在'])

    # 编号 → 词
    print('indices =', vocab[['time', '<pad>', '<unk>']]) # → Vocab.__getitem__(vocab, ['time', '<pad>', '<unk>'])
    print('tokens =', vocab.to_tokens([2, 0, 1])) # → Vocab.to_tokens(vocab, [2, 0, 1])

    # 保存词表到文件
    vocab.save('src/word/vocab.txt')
    print('词表已保存到 src/word/vocab.txt')

    # 从文件加载词表，验证编号一致
    loaded_vocab = Vocab.load('src/word/vocab.txt')
    print('加载后的词表大小:', len(loaded_vocab))
    print("loaded_vocab['time']      =", loaded_vocab['time'])
    print('loaded_vocab.to_tokens([2, 0, 1]) =', loaded_vocab.to_tokens([2, 0, 1]))




if __name__ == '__main__':
    main()