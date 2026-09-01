"""word 包：文本分词（tokenize）与词表（Vocab）。"""

from word.tokenizer import tokenizer
from word.vocabulary import Vocab

__all__ = ['Vocab', 'tokenizer']
