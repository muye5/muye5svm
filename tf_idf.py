#!/usr/bin/env python
#coding=utf-8
from __future__ import division
import os
import sys
import math

feature_word= {}
#############################################################################
#   init feature word set
#############################################################################
def feature_word_init(feature_word_file):
    global feature_word
    f = open(feature_word_file, 'r')
    seqence = 0
    while True:
        term = f.readline()
        if not term: break
        term = term.strip().rstrip(os.sep).split('\t')
        seqence += 1
        feature_word[term[0]] = [seqence, math.log(float(term[1]))]
    f.close()

############################################################################
#   statistic term frequency of word per document
############################################################################
def statistic_frequence(file_name, out):
    global feature_word

    doc_term = dict()
    total_term = 0

    f = open(file_name, 'r')
    while True:
        line = f.readline()
        if not line: break
        terms = line.strip().rstrip(os.sep).split(' ')
        for t in terms:
            total_term += 1
            t = t.strip().split('/')[0].strip()
            if t in feature_word:
                times = doc_term.get(t, 0)
                if times == 0:
                    doc_term[t] = 1
                else:
                    doc_term[t] += 1
    f.close()
    label = file_name.strip().split(os.sep)[-2]
    li = sorted(feature_word.iteritems(), key = lambda d:d[1][0])
    print >> out, label[-2:],
    for t in li:
        if t[0] in doc_term:
            tf = doc_term[t[0]] / total_term
            print >> out, str(t[1][0]) + ':' + str(tf * t[1][1]),
    print >> out

############################################################################
#   pick out all files recursive
############################################################################
def fetch_all_file(dir_name, out):
    files = os.listdir(dir_name)
    for f in files:
        if os.path.isdir(dir_name + os.sep + f):
            fetch_all_file(dir_name + os.sep + f, out)
        else:
            statistic_frequence(dir_name + os.sep + f, out)

############################################################################
#   main module
############################################################################
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: python tf_idf.py dir_name result_file_name feature_word_file"
        sys.exit(-1)

    feature_word_init(sys.argv[3])
    out = open(sys.argv[2], 'w')
    if os.path.isdir(sys.argv[1]):
        fetch_all_file(sys.argv[1], out)
    else:
        statistic_frequence(sys.argv[1], out)
    out.close()

