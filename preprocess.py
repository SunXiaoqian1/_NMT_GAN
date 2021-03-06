# coding:utf8
import numpy as np
import os
import sys
import pandas as pd
from bs4 import BeautifulSoup
import jieba
import pickle
reload(sys)
sys.setdefaultencoding('utf-8')

# read data
current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(current_path)
train_file_en = parent_path + "/data/train/train/train.en"
train_file_zh = parent_path + "/data/train/train/train.zh"
eval_file_en_sgm = parent_path + "/data/eval/eval/valid.en-zh.en.sgm"
eval_file_zh_sgm = parent_path + "/data/eval/eval/valid.en-zh.zh.sgm"
eval_file_zh = eval_file_zh_sgm[:-4]
eval_file_en = eval_file_en_sgm[:-4]
train_file_jieba_zh = train_file_zh[:-3] + '_jieba.zh'
eval_file_jieba_zh = eval_file_zh[:-3] + '_jieba.zh'
train_file_split_en = train_file_en[:-3] + '_split.en'
eval_file_split_en = eval_file_en[:-3] + '_split.en'
src_vocab = "/data/jeicy/data/ec-sjtu/en.vocab"
dst_vocab = '/data/jeicy/data/ec-sjtu/zh.vocab'

#constant
TRAIN = 1
EVAL = 0


# parsing .sgm
def read_sgm(sgm_file):
    # a new file: delete ".sgm"
    filename = sgm_file[:-4]
    output = open(filename, 'w')
    with open(sgm_file, 'r') as f:
        for line in f.readlines():
            soup = BeautifulSoup(line, "html5lib")
            if soup.find('seg'):
                output.write(str(soup.seg.string) + '\n')


# split chinese with jieba
def split_chinese(zh_file):
    lines = []
    zh_jieba_file = zh_file[:-3] + '_jieba.zh'
    with open(zh_file, 'r') as f:
        for line in f.readlines():
            lines.append(line.strip().split('\t'))

    with open(zh_jieba_file, 'w') as f2:
        for line in lines:
            content = line[0].replace(r'[，。！《》（）“”：；？、——’‘]','')
            content = " ".join(jieba.cut(content))
            f2.write(content + '\n')


# split , . in english
def split_english(en_file):
    lines = []
    chs = ['.', ',', '?', '!', '...', ';']
    en_split_file = en_file[:-3] + '_split.en'
    with open(en_file, 'r') as f:
        for line in f.readlines():
            newline = add_space(line, chs)
            lines.append(newline)

    with open(en_split_file, 'w') as f2:
        for line in lines:
            f2.write(line)


# add ' '
def add_space(txt, chs):
    for ch in chs:
        txt = txt.replace(ch, ' ' + ch)
    return txt


def wash_data(en, zh):
    en_wash = en[:-3] + '_wash.en'
    zh_wash = zh[:-3] + '_wash.zh'
    lines_en = []
    lines_zh = []
    with open(en, 'r') as f1:
        line1 = f1.readlines()

    with open(zh, 'r') as f2:
        line2 = f2.readlines()

    for line in line1:
        line2 = line2[line1.index(line)]
        if len(line) > 100 or len(line2) > 100:
            continue
        else:
            lines_en.append(line)
            lines_zh.append(line2)

    with open(en_wash, 'w') as f3:
        for line in lines_en:
            f3.write(line + '\n')

    with open(zh_wash, 'w') as f4:
        for line in lines_zh:
            f4.write(line + '\n')


# put the original and the translated sentences in one line
def joint_original_and_translate(zh_file, en_file, data_mode):
    if data_mode:   # train data
        filename = parent_path + '/data/train/train_file.csv'
    else:   # eval data
        filename = parent_path + '/data/eval/eval_file.csv'

    df = pd.DataFrame()
    original = []
    translated = []

    with open(zh_file, 'r') as zf:
        for zhline in zf.readlines():
            original.append(zhline.strip().split('\n'))

    with open(en_file, 'r') as ef:
        for enline in ef.readlines():
            translated.append(enline.strip().split('\n'))

    df['original'] = original
    df['translated'] = translated

    df.to_csv(filename, index=False, encoding='utf-8', sep='\t')


def vocab_to_pkl(vocab):
    new_vocab = dict()
    pkl_file = vocab + '.pkl'
    with open(vocab, 'r') as v:
        for vocab in v.readlines():
            vocab = vocab.split('\t')
            vocab_int = int(vocab[1])
            new_vocab[vocab[0]] = vocab_int

    with open(pkl_file, 'w') as f:
        pickle.dump(new_vocab, f, protocol=pickle.HIGHEST_PROTOCOL)




if __name__ == '__main__':
    # read_sgm('/Users/jicl/_NMT_GAN/data/test_a/test_a.sgm')
    # read_sgm('/Users/jicl/_NMT_GAN/data/test_b/test_b.sgm')
    # split_chinese('/Users/jicl/_NMT_GAN/data/train/train/train.zh')
    # split_chinese(eval_file_zh)
    # split_english('/Users/jicl/_NMT_GAN/data/test_a/test_a')
    # split_english('/Users/jicl/_NMT_GAN/data/test_b/test_b')
    # wash_data(train_file_en, train_file_zh)
    # wash_data(eval_file_en, eval_file_zh)
    # joint_original_and_translate(train_file_jieba_zh, train_file_en, TRAIN)
    # joint_original_and_translate(eval_file_jieba_zh, eval_file_en, EVAL)
    vocab_to_pkl(src_vocab)
    vocab_to_pkl(dst_vocab)




