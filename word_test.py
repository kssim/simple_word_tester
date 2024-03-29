#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.request import urlopen

from optparse import OptionParser
from random import shuffle
from glob import glob

BASE_URL = 'http://dic.naver.com/search.nhn'

def get_request_uri(keyword):
    uri = '?dicQuery=%s&query=%s&target=dic&ie=utf8&query_utf=&isOnlyViewEE=' % (keyword, keyword)
    return uri

def get_page_source(keyword):
    try:
         response = urlopen(BASE_URL + get_request_uri(keyword))
         return BeautifulSoup(response, 'html.parser')
    except:
        return None

def parse_page_source(soup):
    en_dic_section = soup.find('div', class_='en_dic_section')
    if not en_dic_section:
        return None

    source_word = [s_word.span.getText() for s_word in en_dic_section.find_all('dt')]
    translated_word = [t_word.getText().strip() for t_word in en_dic_section.find_all('dd')]

    return zip(source_word, translated_word)

def get_result(result_tuple):
    if not result_tuple:
        print ("There is no online search result")
        return

    print ("------------------------")
    for s_word, t_word in result_tuple:
        print(f'{s_word}')
        print(f'{t_word}')
    print ("------------------------")

def get_url_encoded_string(translate_string):
    return quote(translate_string)

def search_word(word):
    encoded_word = get_url_encoded_string(word)
    soup = get_page_source(encoded_word)
    if soup:
        get_result(parse_page_source(soup))

def save_word_list(file_path, word_list):
    with open(file_path, "a") as f:
        for word, explanation in word_list.items():
            f.write(f"{word} = {explanation}\n")

def get_word_list(file_path):
    word_list_dic = {}
    with open(file_path, "r") as f:
        for line in f.readlines():
            word = line.strip().split("=")
            if len(word) == 2:
                word_list_dic[word[0].strip()] = word[1].strip()
                continue

            if not word:
                print (f"Error: {word}")

    return word_list_dic

def get_word_files(directory_path):
    return glob(directory_path + "/*.word")

def practice():
    while True:
        if input() == "n":
            break

def add_word_list(file_path):
    word_list = {}
    try:
        while True:
            print ("========================")
            word = input("Input a word : ")
            search_word(word)
            explanation = input("Input a explation : ")

            if word.strip() and explanation.strip():
                word_list[word] = explanation
    except KeyboardInterrupt:
        print ("Quit the program")
    finally:
        save_word_list(file_path, word_list)

def word_test(word_list_dic, reverse, practice_mode):
    words = list(word_list_dic.keys())
    shuffle(words)

    total_count = 0
    answer_count = 0

    try:
        for i, word in enumerate(words):
            if i == 100:
                raise KeyboardInterrupt()

            print ("===========")
            print (f"{i+1}. {word_list_dic[word] if reverse else word}")
            user_input = input()

            total_count += 1
            answer = word if reverse else word_list_dic[word]
            print (answer)

            if user_input == answer:
                answer_count += 1
            elif practice_mode:
                practice()

            print ("===========")
            print ("\n")
    except KeyboardInterrupt:
        print ("Quit the program")
    finally:
        print (f"{answer_count}/{total_count} ({answer_count/total_count*100:.1f}%)")


def main():
    parser = OptionParser("Usage: %prog ")
    parser.add_option("-f", "--file", dest="file_path", help="word file location")
    parser.add_option("-r", "--reverse", dest="reverse", action="store_true", help="word & meaning reverse")
    parser.add_option("-d", "--directory", dest="directory_path", help="word file directy")
    parser.add_option("-p", "--practice", dest="practice_mode", action="store_true", help="set the practice mode")
    parser.add_option("-a", "--add_mode", dest="add_mode", action="store_true", help="set the add mode")

    (options, _) = parser.parse_args()

    if options.file_path and options.directory_path:
        parser.print_help()
        exit(1)
    elif options.file_path and options.add_mode:
        add_word_list(options.file_path)
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
