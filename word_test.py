#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from random import shuffle

def get_word_list(file_path):
    word_list_dic = {}
    with open(file_path, "r") as f:
        for line in f.readlines():
            word = line.strip().split("=")
            if len(word) == 2:
                word_list_dic[word[0].strip()] = word[1].strip()
                continue

            if not word:
                print ("Error: %s" %  word)

    return word_list_dic

def word_test(word_list_dic, reverse):
    words = list(word_list_dic.keys())
    shuffle(words)

    for word in words:
        print ("===========")
        print (word_list_dic[word] if reverse else word)
        input()
        print (word if reverse else word_list_dic[word])
        print ("===========")
        print ("\n")

def main():
    option = OptionParser("Usage: %prog ")
    option.add_option("-f", "--file", dest="file_path", help="word file location")
    option.add_option("-r", "--reverse", dest="reverse", action="store_true", help="word file location")

    (options, _) = option.parse_args()

    if not options.file_path:
        exit(1)

    word_test(get_word_list(options.file_path), options.reverse)


if __name__ == "__main__":
    main()
