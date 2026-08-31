class Vocab:
    """词表：建立词→编号的映射，支持 <pad> 和 <unk>"""
    # 特殊标记定义为类属性，实例与 load 类方法共用
    pad, unk = '<pad>', '<unk>'

    def __init__(self, tokens=None, min_freq=1, reserved_tokens=None):
        # 特殊标记统一放在最前面，索引从 0 开始
        # list[str]
        self.idx_to_token = [self.pad, self.unk] # ['<pad>', '<unk>', ...]
        # dict[str, int]
        self.token_to_idx = {token: idx for idx, token in enumerate(self.idx_to_token)} # {'<pad>': 0, '<unk>': 1, ...}

        # 追加用户额外预留的特殊标记（如 <bos>、<eos>）
        for token in (reserved_tokens or []):
            self._insert(token)

        # 统计词频，只保留频次 >= min_freq 的词，按频次降序加入
        if tokens is not None:
            counter = {} # 统计词频的字典
            for line in tokens:
                for token in line:
                    counter[token] = counter.get(token, 0) + 1
            for token, freq in sorted(counter.items(), key=lambda x: x[1], reverse=True):
                # 如果词频 >= min_freq，加入词表
                if freq >= min_freq:
                    self._insert(token)

    def _insert(self, token):
        """把新词加入词表（若已存在则跳过）"""
        if token not in self.token_to_idx:
            self.token_to_idx[token] = len(self.idx_to_token) # to dict
            self.idx_to_token.append(token) # to list

    def __len__(self):
        return len(self.idx_to_token)

    def __getitem__(self, tokens):
        """词 → 编号；不在词表的词归为 <unk>"""
        if isinstance(tokens, (list, tuple)):
            return [self.__getitem__(token) for token in tokens]
        return self.token_to_idx.get(tokens, self.token_to_idx[self.unk])

    def to_tokens(self, indices):
        """编号 → 词"""
        if isinstance(indices, (list, tuple)):
            return [self.to_tokens(i) for i in indices]
        return self.idx_to_token[indices]

    def save(self, path):
        """把词表保存到文件，每行一个词，顺序即编号"""
        with open(path, 'w', encoding='utf-8') as f:
            for token in self.idx_to_token:
                f.write(token + '\n')

    @classmethod
    def load(cls, path):
        """从文件加载词表，恢复 <pad>/<unk> 和编号顺序"""
        with open(path, encoding='utf-8') as f:
            tokens = [line.strip() for line in f if line.strip()]

        # 校验文件头部是 <pad>、<unk>，避免编号错位
        if tokens[:2] != [cls.pad, cls.unk]:
            raise ValueError(f"词表文件头部应为 {cls.pad}、{cls.unk}，当前为 {tokens[:2]}")

        vocab = cls()  # 先建默认 [<pad>, <unk>]
        vocab.idx_to_token = tokens
        vocab.token_to_idx = {token: i for i, token in enumerate(tokens)}
        return vocab