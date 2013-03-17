#!/usr/bin/env python
#coding=utf-8
from __future__ import division
import os
import sys

tokens_dict = {}
doc_dict = {}
doc_num = {}

############################################################################
#   read tokens from file_name into doc_dict
############################################################################
def read_tokens(file_name):
    global doc_dict
    global doc_num
    f = open(file_name, 'r')
    doc_tokens = {}
    total_doc = 0
    line_num = 0
    while True:
        line = f.readline();
        if not line: break
        line_num += 1
        terms = line.strip().split('\t')
        if len(terms) != 3:
            print file_name, line_num, terms
            sys.exit(-1)
        word, frequency, left = terms[0:3]
        doc_tokens[word] = [int(frequency), int(left)]
        total_doc = int(frequency) + int(left)
    f.close()
    doc_dict[file_name] = doc_tokens
    doc_num[file_name] = total_doc

############################################################################
#   pick out all files recursive
############################################################################
def fetch_all_file(dir_name):
    files = os.listdir(dir_name)
    for f in files:
        if os.path.isdir(dir_name + os.sep + f):
            fetch_all_file(dir_name + os.sep + f)
        else:
            read_tokens(dir_name + os.sep + f)

############################################################################
#   extract the feature by counting X^2
############################################################################
def extract_feature(dir_name):
    global doc_dict
    global doc_num
    global tokens_dict
    for doc in doc_dict:
        tmp_dict = {}
        for token in doc_dict[doc]:
            other_include_doc = 0
            other_exclude_doc = 0
            for other_doc in doc_dict:
                if doc != other_doc:
                    l = doc_dict[other_doc].get(token, [])
                    if len(l) == 0:
                        other_exclude_doc += doc_num[other_doc]
                    else:
                        other_include_doc += l[0]
                        other_exclude_doc += l[1]
            tmp_dict[token] =doc_dict[doc][token][0:]
            tmp_dict[token].extend([other_include_doc, other_exclude_doc])
        tokens_dict[doc] = tmp_dict
    #----------------------------------------------------------------------#
    #   extract top 1000 word
    #----------------------------------------------------------------------#
    N = 0
    for t in doc_num:
        N += doc_num[t]

    for doc in tokens_dict:
        tmp = {}
        for t in tokens_dict[doc]:
            if len(tokens_dict[doc][t]) != 4:
                print "Wrong in tokens_dict:", doc, t, tokens_dict[doc][t]
                sys.exit(-1)
            else:
                l = tokens_dict[doc][t]
                z1 = l[0] * l[3] - l[1] * l[2]
                x2 = (z1 * z1 * N) / ((l[0] + l[1]) * (l[0] + l[2]) * (l[2] + l[3]) * (l[1] + l[3]))
                tmp[t] = [x2, N / (l[0] + l[2])]
        output(dir_name, doc, tmp)

############################################################################
#   output the result
############################################################################
def output(out_dir, source_file, tokens):
    file_name = source_file.strip().split(os.sep)[-1]
    out = open(out_dir + os.sep + file_name, 'w')
    li = sorted(tokens.iteritems(), key = lambda d:d[1][0], reverse = True)
    for i in range(3000):
        print >> out, li[i][0] + '\t' + str(li[i][1][1])
    out.close()
############################################################################
#   main module
############################################################################
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: python top_words.py dir_name result_dir"
        sys.exit(-1)

    if os.path.isdir(sys.argv[1]):
        fetch_all_file(sys.argv[1])
    else:
        print "Invalid dir_name"
        sys.exit(-1)
    extract_feature(sys.argv[2])
