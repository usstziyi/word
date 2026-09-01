"""极简语言模型：目前只有一层 Embedding（词向量查表）。"""

import torch
import torch.nn as nn


class LLM(nn.Module):
    """极简语言模型，``vocab_size`` 必须与词表大小一致。

    Attributes:
        vocab_size: 词表大小。
        hidden_size: 每个 token 向量的维度。
        embedding: 词向量层，权重形状 ``[vocab_size, hidden_size]``，
            每行对应一个词的向量。
    """

    def __init__(self, vocab_size: int, hidden_size: int = 8) -> None:
        super().__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(vocab_size, hidden_size)

    def forward(self, indices: torch.Tensor) -> torch.Tensor:
        """输入 token 编号，输出对应的词向量。

        Args:
            indices: token 编号张量（dtype 必须为 ``torch.long``），
                支持标量、一维或多维 batch。

        Returns:
            词向量张量，形状为 ``indices.shape + [hidden_size]``。
        """
        return self.embedding(indices)

