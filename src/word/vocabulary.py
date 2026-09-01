"""词表（Vocabulary）：建立 token ↔ 编号 的双向映射。"""

from collections.abc import Sequence
from typing import ClassVar

Token = str
Tokens = Sequence[Token]


class Vocab:
    """词表：建立词→编号的映射，支持 ``<pad>`` 和 ``<unk>``。

    特殊标记统一放在最前面（索引从 0 开始）：``<pad>=0``、``<unk>=1``。
    不在词表中的词会映射到 ``<unk>``。

    Attributes:
        idx_to_token: 编号 → 词 的列表，列表下标即编号。
        token_to_idx: 词 → 编号 的字典。
    """

    # 特殊标记定义为类属性，实例与 load 类方法共用
    pad: ClassVar[str] = '<pad>'
    unk: ClassVar[str] = '<unk>'

    def __init__(
        self,
        tokens: Sequence[Tokens] | None = None,
        min_freq: int = 1,
        reserved_tokens: Sequence[Token] | None = None,
    ) -> None:
        """建立词表。

        Args:
            tokens: 分好词的二维序列（每行一个 token 列表）。为 ``None`` 时
                只包含特殊标记。
            min_freq: 词频低于该值的词不会加入词表。
            reserved_tokens: 额外预留的特殊标记（如 ``<bos>``、``<eos>``），
                会紧跟 ``<pad>``/``<unk>`` 插入。
        """
        self.idx_to_token: list[Token] = [self.pad, self.unk]  # ['<pad>', '<unk>', ...]
        self.token_to_idx: dict[Token, int] = {token: idx for idx, token in enumerate(self.idx_to_token)}  # {'<pad>': 0, '<unk>': 1, ...}

        # 追加用户额外预留的特殊标记（如 <bos>、<eos>）
        for token in reserved_tokens or ():
            self._insert(token)

        # 统计词频，只保留频次 >= min_freq 的词，按频次降序加入
        if tokens is not None:
            counter: dict[Token, int] = {}  # 统计词频的字典
            for line in tokens:
                for token in line:
                    counter[token] = counter.get(token, 0) + 1
            for token, freq in sorted(counter.items(), key=lambda x: x[1], reverse=True):
                if freq >= min_freq:
                    self._insert(token)

    def _insert(self, token: Token) -> None:
        """把新词加入词表（若已存在则跳过）。

        Args:
            token: 要加入的词。
        """
        if token not in self.token_to_idx:
            self.token_to_idx[token] = len(self.idx_to_token)
            self.idx_to_token.append(token)

    def __len__(self) -> int:
        """词表大小（含特殊标记）。"""
        return len(self.idx_to_token)

    def __getitem__(self, tokens: Token | Tokens) -> int | list[int]:
        """词 → 编号；不在词表的词归为 ``<unk>``。

        传入单个词返回单个编号，传入列表/元组返回编号列表。

        Args:
            tokens: 单个词，或词的列表/元组。

        Returns:
            对应的编号（或编号列表）。
        """
        if isinstance(tokens, Sequence) and not isinstance(tokens, str):
            return [self.__getitem__(token) for token in tokens]
        return self.token_to_idx.get(tokens, self.token_to_idx[self.unk])

    def to_tokens(self, indices: int | Sequence[int]) -> Token | list[Token]:
        """编号 → 词。

        传入单个编号返回单个词，传入列表/元组返回词列表。

        Args:
            indices: 单个编号，或编号的列表/元组。

        Returns:
            对应的词（或词列表）。
        """
        if isinstance(indices, Sequence) and not isinstance(indices, str):
            return [self.to_tokens(i) for i in indices]
        return self.idx_to_token[indices]

    def save(self, path: str) -> None:
        """把词表保存到文件，每行一个词，顺序即编号。

        Args:
            path: 输出文件路径（UTF-8）。
        """
        with open(path, 'w', encoding='utf-8') as f:
            for token in self.idx_to_token:
                f.write(token + '\n')

    @classmethod
    def load(cls, path: str) -> 'Vocab':
        """从文件加载词表，恢复 ``<pad>``/``<unk>`` 和编号顺序。

        Args:
            path: 词表文件路径（UTF-8，每行一个词）。

        Returns:
            加载后的 :class:`Vocab` 实例。

        Raises:
            ValueError: 文件头部不是 ``<pad>``、``<unk>``，可能导致编号错位。
        """
        with open(path, encoding='utf-8') as f:
            tokens = [line.strip() for line in f if line.strip()]

        # 校验文件头部是 <pad>、<unk>，避免编号错位
        if tokens[:2] != [cls.pad, cls.unk]:
            raise ValueError(f"词表文件头部应为 {cls.pad}、{cls.unk}，当前为 {tokens[:2]}")

        vocab = cls()  # 先建默认 [<pad>, <unk>]
        vocab.idx_to_token = tokens
        vocab.token_to_idx = {token: i for i, token in enumerate(tokens)}
        return vocab