#!/usr/bin/env python
#coding=utf-8
import os
import sys

word_dict = {}
stop_word = set([])
num_doc = 0
#############################################################################
#   init stop word set
#############################################################################
def stop_word_init(stop_word_file):
    global stop_word
    f = open(stop_word_file, 'r')
    tmp = []
    while True:
        term = f.readline()
        if not term: break
        term = term.strip().rstrip(os.sep)
        tmp.append(term)
    f.close()
    stop_word = set(tmp)
############################################################################
#   statistic term frequency of word per document
############################################################################
def statistic_frequence(file_name):
    global word_dict
    global stop_word
    global num_doc

    doc_term = dict()
    total_term = 0

    f = open(file_name, 'r')
    while True:
        line = f.readline()
        if not line: break
        terms = line.strip().rstrip(os.sep).split(' ')
        for t in terms:
            t = t.strip().split('/')[0].strip()
            if t not in stop_word:
                times = doc_term.get(t, 0)
                if times == 0:
                    doc_term[t] = 1
                else:
                    doc_term[t] += 1
    f.close()

    num_doc += 1
    for t in doc_term:
        times = word_dict.get(t, 0)
        if times == 0:
            word_dict[t] = 1
        else:
            word_dict[t] += 1

############################################################################
#   pick out all files recursive
############################################################################
def fetch_all_file(dir_name):
    files = os.listdir(dir_name)
    for f in files:
        if os.path.isdir(dir_name + os.sep + f):
            fetch_all_file(dir_name + os.sep + f)
        else:
            statistic_frequence(dir_name + os.sep + f)

############################################################################
#   main module
############################################################################
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: python feature_extract.py dir_name result_file_name stop_word_file"
        sys.exit(-1)

    stop_word_init(sys.argv[3])

    if os.path.isdir(sys.argv[1]):
        fetch_all_file(sys.argv[1])
    else:
        statistic_frequence(sys.argv[1])

    out = open(sys.argv[2], 'w')
    tuple_list = sorted(word_dict.items(), key = lambda d:d[1], reverse = True)
    for term in tuple_list:
        print >> out, term[0] + '\t' + str(term[1]) + '\t' + str(num_doc - term[1])
    out.close()

