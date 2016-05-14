#!/usr/bin/env python
# coding=utf-8
#中译英

import json
import nltk
import numpy as np
from nltk.translate import ibm1,AlignedSent,Alignment,PhraseTable,stack_decoder


def translation_model_generation():
    bilingual_text = []
    english_file = open("english_tokens.json","r")
    english_text = english_file.read()
    english_list = json.loads(english_text)
    chinese_file = open("chinese_tokens.json","r")
    chinese_text = chinese_file.read()
    chinese_list = json.loads(chinese_text)
    for iter in zip(chinese_list,english_list):
        bilingual_text.append(AlignedSent(iter[0],iter[1]))
    ibm1_model = ibm1.IBMModel1(bilingual_text,10)
    return ibm1_model

def language_model_generation():
    chinese_file = open("chinese_tokens.json","r")
    chinese_text = chinese_file.read()
    chinese_list = json.loads(chinese_text)
    fdist = nltk.FreqDist(w for sentence in chinese_list for w in sentence)
    
    fdist.setdefault(lambda:1e-300)
    language_model = type('',(object,),{'probability_change':lambda self,context,phrase:np.log(fdist[phrase]),'probability':lambda self,phrase:np.log(fdist[phrase])})()
    return language_model

def phrase_table_generation(ibm1_model):
    phrase_table = PhraseTable()
    for chinese_word in ibm1_model.translation_table.keys():
        for english_word in ibm1_model.translation_table[chinese_word].keys():
            phrase_table.add(chinese_word,english_word,np.log(ibm1_model.translation_table[chinese_word][english_word]))

    return phrase_table


if __name__ == '__main__':
#    test_sentence = bilingual_text[2]
#    print(test_sentence.words)
#    print(test_sentence.mots)
#    print(test_sentence.alignment)
    phrase_table = phrase_table_generation(translation_model_generation())
    language_model = language_model_generation()
    stack_decoder1 = stack_decoder.StackDecoder(phrase_table,language_model)  
    print(stack_decoder1.translate(["中国","国家","主席","习近平","。"]))

