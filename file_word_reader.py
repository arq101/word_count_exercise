#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import operator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s -- %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',)
logger = logging.getLogger(__name__)

READ_FILES_FROM_PATH = '.'
OUTPUT_RESULTS_PATH = './word_count_output'
_all_words_read = {}
_words_read_from_each_file = {}


def _read_words_from_file(filename):
    """
    Performs a tally of each word encountered across all files and collects a unique list of
    words per file.
    """
    logger.info('Reading words from: {}'.format(filename))
    with open(filename, 'r') as fh:
        words_encountered = []
        for line in fh:
            words = line.split()
            for word in words:
                word = word.strip('",')
                if word in _all_words_read:
                    _all_words_read[word] += 1
                else:
                    _all_words_read[word] = 1
                words_encountered.append(word)
    _words_read_from_each_file[filename] = set(words_encountered)


def _get_list_of_files(file_path):
    """
    Gets a list of files in the given directory path.
    """
    logger.info('Reading files ...')
    files = [file for file in os.listdir(file_path)
             if os.path.isfile(file) and not file.startswith('.') and not file.endswith('.py') and
             not file.endswith('_output')]

    if files:
        logger.info('Files found: {}'.format([f for f in files]))
    else:
        logger.info('No files found. Exiting!')
        sys.exit(0)
    return files


def _get_top_occurring_words(int_val):
    """
    Gets a list of the most frquent words by sorting the dictionary based on its values.
    Returns a list of tuples with a word and its frequency.
    """
    top_words = sorted(_all_words_read.items(), key=operator.itemgetter(1), reverse=True)
    return top_words[:int_val]


def _get_all_intersecting_words():
    """
    Returns a set of words that occur across all files.
    """
    word_sets = [words for words in _words_read_from_each_file.values()]
    return set.intersection(*word_sets)


def _get_word_difference_per_file():
    """
    Returns a list with sets of words that are unique to each file.
    """
    word_sets = {file_name: words for file_name, words in _words_read_from_each_file.items()}

    # TODO -- needs a far better way, should handle dict object dynamically
    word_sets['file_1.txt'] = word_sets['file_1.txt'].difference(word_sets['file_2.txt']).\
        difference(word_sets['file_3.txt'])
    word_sets['file_2.txt'] = word_sets['file_2.txt'].difference(word_sets['file_1.txt']).\
        difference(word_sets['file_3.txt'])
    word_sets['file_3.txt'] = word_sets['file_3.txt'].difference(word_sets['file_1.txt']).\
        difference(word_sets['file_2.txt'])
    return word_sets


def _write_output(top_words, intersecting_words, unique_words):
    """
    Writes the output to a file.

    :param top_words:
        list containing contains tuples, eg. ('some_word' 1).
    :param intersecting_words:
        set object
    :param unique_words:
        dict object with file_name and word set as k, v pair.
    """
    logger.info('Writing results to: {}'.format(OUTPUT_RESULTS_PATH))
    with open(OUTPUT_RESULTS_PATH, 'w') as f_results:
        f_results.write(">> 1) Most Frequent Words\n")
        for item in top_words:
            f_results.write("{:<20} {:<20}\n".format(item[0], item[1]))
        f_results.write("\n\n")

        f_results.write(">> 2) {} Intersecting Words Found Across All Files\n".format(
            len(intersecting_words)))
        for word in sorted(intersecting_words):
            f_results.write(word + "\n")
        f_results.write("\n\n")

        f_results.write(">> 3) Words unique to each file\n")
        for file_name, word_set in unique_words.items():
            f_results.write(file_name + ': ' + str(len(word_set)) + "\n")
        f_results.write("\n")

        for file_name, word_set in unique_words.items():
            f_results.write("{} unique words:\n".format(file_name))
            for word in sorted(word_set):
                f_results.write(word + "\n")
            f_results.write("\n")


def main():
    files = _get_list_of_files(READ_FILES_FROM_PATH)
    for f in files:
        _read_words_from_file(f)

    top_words_list = _get_top_occurring_words(10)
    intersecting_words = _get_all_intersecting_words()
    word_difference = _get_word_difference_per_file()
    _write_output(top_words_list, intersecting_words, word_difference)

    logger.info('Process complete.')


if __name__ == '__main__':
    main()
