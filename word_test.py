#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from random import shuffle
from glob import glob


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

def get_word_files(directory_path):
    return glob(directory_path + "/*.word")

def word_test(word_list_dic, reverse):
    words = list(word_list_dic.keys())
    shuffle(words)

    for i, word in enumerate(words):
        print ("===========")
        print ("%s. %s" % (i+1, word_list_dic[word] if reverse else word))
        input()
        print (word if reverse else word_list_dic[word])
        print ("===========")
        print ("\n")

def main():
    option = OptionParser("Usage: %prog ")
    option.add_option("-f", "--file", dest="file_path", help="word file location")
    option.add_option("-r", "--reverse", dest="reverse", action="store_true", help="word & meaning reverse")
    option.add_option("-d", "--directory", dest="directory_path", help="word file directy")

    (options, _) = option.parse_args()

    if options.file_path and options.directory_path:
        exit(1)
    elif options.file_path:
        word_test(get_word_list(options.file_path), options.reverse)
    elif options.directory_path:
        word_list = {}
        for word_file in get_word_files(options.directory_path):
            word_list.update(get_word_list(word_file))

        word_test(word_list, options.reverse)


if __name__ == "__main__":
    main()
