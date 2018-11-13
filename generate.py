import helper
import re
# dir = 'data/寒门首辅.txt'
# text = helper.load_text(dir)
num_words_for_training = 1053095
# text = text[:num_words_for_training]
# lines_of_text = text.split('\n')
# print(len(lines_of_text))
#
with open('../data/bible.txt', 'rt', encoding='utf-8') as f:
    text = f.read()

text = text[:num_words_for_training]
lines_of_text = text.split('\n')
lines_of_text = lines_of_text[0:]
lines_of_text = [lines for lines in lines_of_text if len(lines) > 0]
# 去掉每行首尾空格
lines_of_text = [lines.strip() for lines in lines_of_text]
pattern = re.compile(r'\[.*\]')
lines_of_text = [pattern.sub("", lines) for lines in lines_of_text]
# 将上面的正则换成负责找『<>』包含的内容
pattern = re.compile(r'<.*>')
# 将所有指定内容替换成空
lines_of_text = [pattern.sub("", lines) for lines in lines_of_text]
# 将上面的正则换成负责找『......』包含的内容
pattern = re.compile(r'\.+')
# 将所有指定内容替换成空
lines_of_text = [pattern.sub("。", lines) for lines in lines_of_text]
# 将上面的正则换成负责找句尾『\\r』的内容
pattern = re.compile(r'\\r')
# 将所有指定内容替换成空
lines_of_text = [pattern.sub("", lines) for lines in lines_of_text]

def create_lookup_tables(input_data):
    vocab = set(input_data)
    # 文字到数字的映射
    vocab_to_int = {word: idx for idx, word in enumerate(vocab)}
    # 数字到文字的映射
    int_to_vocab = dict(enumerate(vocab))
    return vocab_to_int, int_to_vocab

def token_lookup():
    symbols = set(['。', '，', '“', "”", '；', '！', '？', '（', '）', '——', '\n'])
    tokens = ["P", "C", "Q", "T", "S", "E", "M", "I", "O", "D", "R"]
    return dict(zip(symbols, tokens))

helper.preprocess_and_save_data(''.join(lines_of_text), token_lookup, create_lookup_tables)
int_text, vocab_to_int, int_to_vocab, token_dict = helper.load_preprocess()

print(len(lines_of_text))