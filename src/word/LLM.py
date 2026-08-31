import torch
import torch.nn as nn



class LLM(nn.Module):

    def __init__(self, vocab_size, hidden_size=8):
        super().__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(vocab_size, hidden_size) # weight shape: [vocab_size, hidden_size]  ← 每行是一个词的向量

    def forward(self, indices):
        return self.embedding(indices)

