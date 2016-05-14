#!/usr/bin/env python
# coding=utf-8

from nltk.tokenize import word_tokenize
import json
import jieba

english_file = open("english_corpus.json","r")
english_text = english_file.read()
english_corpus = json.loads(english_text)
english_tokens = []
for sentence in english_corpus:
    english_tokens.append(word_tokenize(sentence))

english_tokens_json = json.dumps(english_tokens)
f1 = open("english_tokens.json","w")
f1.write(english_tokens_json)
f1.close()
print(english_tokens[5565])

chinese_file = open("chinese_corpus.json","r")
chinese_text = chinese_file.read()
chinese_corpus = json.loads(chinese_text)
chinese_tokens = []
for sentence in chinese_corpus:
    chinese_tokens.append(jieba.lcut(sentence,cut_all=False))

chinese_tokens_json = json.dumps(chinese_tokens)
f2 = open("chinese_tokens.json","w")
f2.write(chinese_tokens_json)
f2.close()
print(chinese_tokens[5565])

