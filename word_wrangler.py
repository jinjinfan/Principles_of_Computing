"""
Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    returned_list =[]
    item_ = ""
    for item in list1:
        if item!= item_:
            item_ = item
            returned_list.append(item_)
    return returned_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    returned_list = []
    idx1 = idx2 = 0
    while idx1 < len(list1) and idx2 < len(list2):
        if list2[idx2] > list1[idx1]:
            idx1 += 1
        elif list2[idx2] < list1[idx1]:
            idx2 += 1
        elif list2[idx2] == list1[idx1]:
            returned_list.append(list1[idx1])
            idx1 += 1
            idx2 += 1
    return returned_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    returned_list = []
    idx1 = idx2 = 0
    while idx1 < len(list1) and idx2 < len(list2):
        if list2[idx2] > list1[idx1]:
            returned_list.append(list1[idx1])
            idx1 += 1
        else:
            returned_list.append(list2[idx2])
            idx2 += 1
    if idx1 == len(list1):
        for index in range(idx2, len(list2)):
            returned_list.append(list2[index])
    else:
        for index in range(idx1, len(list1)):
            returned_list.append(list1[index])
    return returned_list

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if list1 == []:
        return []
    else:
        pivot = list1[0]
        lesser = [item for item in list1 if item < pivot]
        pivots = [item for item in list1 if item == pivot]
        greater = [item for item in list1 if item > pivot]
        return merge_sort(lesser) + pivots + merge_sort(greater)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [""]
    first = word[0]
    rest_strings = gen_all_strings(word[1:])
    newstring = list(rest_strings)
    for item in rest_strings:
        newstring.append(first + item)
        for index in range(len(item)-1):
            newstring.append(item[:index+1] + first + item[index+1:])
        if item != "":
            newstring.append(item + first)
    return newstring
# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    string_lists = []
    for line in netfile.readlines():
        string_lists.append(line[:-1])
    return string_lists

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()