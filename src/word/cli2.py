import torch
from word.LLM import LLM
from word.vocabulary import Vocab

# 1. 加载词表 + 实例化（vocab_size 必须和词表一致）
vocab = Vocab.load('src/word/vocab.txt')
model = LLM(vocab_size=len(vocab), hidden_size=8)
model.eval()

# 2. 构造索引张量 —— 必须是 long 类型
indices = torch.tensor([vocab['time'], vocab['machine'], vocab['<pad>']],
                       dtype=torch.long)


# 3. 前向：输出每个 token 的向量
with torch.no_grad():
    # 一维
    indices = torch.tensor([vocab['time'], vocab['machine'], vocab['<pad>']],
                       dtype=torch.long)
    vecs = model(indices)   # shape: [3, 8]
    print(vecs.shape)

    # 一维
    vec = model(torch.tensor([vocab['time']], dtype=torch.long))  # shape: [8]
    print(vec.shape)

    # 标量
    vec = model(torch.tensor(vocab['time'], dtype=torch.long))  # shape: [8]
    print(vec.shape)

    # 二维（batch：2 行 × 3 列）
    batch = torch.tensor([
        [vocab['time'], vocab['machine'], vocab['<pad>']],
        [vocab['machine'], vocab['<pad>'], vocab['<unk>']],
    ], dtype=torch.long)  # shape: [2, 3]
    vecs = model(batch)   # shape: [2, 3, 8]
    print(vecs.shape)





