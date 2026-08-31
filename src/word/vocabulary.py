class Vocab:
    """词表：建立词→编号的映射，支持 <pad> 和 <unk>"""

    def __init__(self, tokens=None, min_freq=1, reserved_tokens=None):
        # 特殊标记统一放在最前面，索引从 0 开始
        self.unk, self.pad = '<unk>', '<pad>'
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