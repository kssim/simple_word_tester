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

def practice():
    while True:
        if input() == "n":
            break

def word_test(word_list_dic, reverse, practice_mode):
    words = list(word_list_dic.keys())
    shuffle(words)

    for i, word in enumerate(words):
        print ("===========")
        print ("%s. %s" % (i+1, word_list_dic[word] if reverse else word))
        user_input = input()
        answer = word if reverse else word_list_dic[word]
        print (answer)
        if practice_mode and user_input != answer:
            practice()

        print ("===========")
        print ("\n")

def main():
    parser = OptionParser("Usage: %prog ")
    parser.add_option("-f", "--file", dest="file_path", help="word file location")
    parser.add_option("-r", "--reverse", dest="reverse", action="store_true", help="word & meaning reverse")
    parser.add_option("-d", "--directory", dest="directory_path", help="word file directy")
    parser.add_option("-p", "--practice", dest="practice_mode", action="store_true", help="set the practice mode")

    (options, _) = parser.parse_args()

    if options.file_path and options.directory_path:
        parser.print_help()
        exit(1)
    elif options.file_path:
        word_test(get_word_list(options.file_path), options.reverse, options.practice_mode)
    elif options.directory_path:
        word_list = {}
        for word_file in get_word_files(options.directory_path):
            word_list.update(get_word_list(word_file))

        word_test(word_list, options.reverse, options.practice_mode)
    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()
