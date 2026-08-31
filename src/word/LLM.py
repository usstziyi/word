import torch
import torch.nn as nn

from word.vocabulary import Vocab
from word.tokenizer import tokenizer


def device_setup():
    if torch.cuda.is_available():
        return torch.device('cuda')
    if torch.backends.mps.is_available():
        return torch.device('mps')
    return torch.device('cpu')


class LLM(nn.Module):

    def __init__(self, vocab_size, hidden_size=8):
        super().__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(vocab_size, hidden_size) # weight shape: [vocab_size, hidden_size]  ← 每行是一个词的向量

    def forward(self, indices):
        return self.embedding(indices)


if __name__ == '__main__':

    device = device_setup()
    print(f'当前设备: {device}')


    with open('src/book/input.txt', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    vocab = Vocab(tokenizer(lines, token='word'))
    print('词表大小:', len(vocab))

    model = LLM(vocab_size=len(vocab), hidden_size=8).to(device)
    print(model)

    vec = model(torch.tensor(vocab['time'], device=device))
    print(f"vec.shape = {vec.shape}")

    indices = torch.tensor(vocab[['time', 'machine', '<pad>', '<unk>']], device=device)
    vecs = model(indices)
    print(f"vecs.shape = {vecs.shape}")

    for tok, v in zip(['time', 'machine', '<pad>', '<unk>'], vecs):
        print(f'{tok!r} 向量 -> {v.tolist()}')