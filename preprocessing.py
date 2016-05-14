#!/usr/bin/env python
# coding=utf-8

import json
import glob
import re

def fileload(filename):
    '''这个函数将每个文件当中的同一篇文章整合到一个字典，
    字典中仍然有3个索引'''

    f = open(filename,"r")
    file = f.read()

    text = {"article":[]}
    position = 0
    while position<len(file):
        location = file.find("}",position)+1
        dict = json.loads(file[position:location])
        position = location
        text["english_title"] = dict["english_title"]
        text["chinese_title"] = dict["chinese_title"]
#        print(type(text["article"]))
        text["article"].extend(dict["article"])
#       text["article"] = text["article"].extend(dict["article"])  为什么是错误的？
    return text

def preprocess(text):
    '''这个函数将文章中的中英文分开，包含标题。'''
    chinese_corpus = []
    english_corpus = []
    pattern = re.compile('[\u4e00-\u9fa5]')
    chinese_corpus.append(text["chinese_title"].strip())
    english_corpus.append(text["english_title"].strip())
    for phase in text["article"]:
        try:
            position = pattern.search(phase).span()[0]
            english_corpus.append(phase[:position].strip())
            chinese_corpus.append(phase[position:].strip())
        except:
            continue
    return chinese_corpus,english_corpus

def concatenate():
    '''这个函数将所有文章整合成一个语料库，以句为基元，失去了篇章信息'''
    filelist = glob.glob('[0-9]*-*')
    print(len(filelist))
    chinese_corpus = []
    english_corpus = []
    for file in filelist:
        text = fileload(file)
        chinese,english = preprocess(text)
        chinese_corpus.extend(chinese)
        english_corpus.extend(english)
    return chinese_corpus,english_corpus



if __name__ == "__main__":
    a,b =  preprocess(fileload("a"))
    print(a[0],b[0],a[1],b[1],a[10],b[10])
    chinese_corpus,english_corpus = concatenate()
    print(len(chinese_corpus),len(english_corpus))
    print(chinese_corpus[100],english_corpus[100])
    chinese_json = json.dumps(chinese_corpus)
    f1 = open("chinese_corpus.json","w")
    f1.write(chinese_json)
    f1.close()
    english_json = json.dumps(english_corpus)
    f2 = open("english_corpus.json","w")
    f2.write(english_json)
    f2.close()
