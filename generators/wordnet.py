'''
    Passphrase generator that uses WordNet.

    Copyright (C) 2015 jonathan lung <lungj+git@heresjono.com>
    
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

from __future__ import division, with_statement, print_function, generators
from math import log

import nltk
from nltk.corpus import wordnet
from pattern.en import pluralize, conjugate, PAST, PRESENT, PLURAL

from entropy.random import randint, random_item_from_list

def trans_verb_list():
    '''Generate a list of transitive verbs.'''
    transitive_verbs = []
    for word in wordnet.all_lemma_names('v'):
        frame_ids = set()
        for lem in wordnet.lemmas(word, 'v'):
            frame_ids.update(lem.frame_ids())
        # Verbs with these frames make sense for our sentences.
        if frame_ids.intersection({8, 9, 10, 11}):
            transitive_verbs.append(word)

    # Remove duplicates by converting to set and back in case of
    # malicious WordNet.
    return list(set(transitive_verbs))


def words_of_type(word_type, min_frequency=4):
    '''
    Generate a list of words of WordNet word_type that have a total frequency of at least
    min_frequency times across all senses of the word with word_type.
    '''
    try:
        with open(word_type + '.' + str(min_frequency), 'r') as file:
            return file.read().split('\n')
    except:
        words = []
        for word in wordnet.all_lemma_names(wordnet.__getattribute__(word_type)):
            counts = [lem.count() for lem in wordnet.lemmas(word, wordnet.__getattribute__(word_type))]

            if sum(counts) >= min_frequency:
                words.append(word)

        words = [item for item in words if not item.isdigit()]

        with open(word_type + '.' + str(min_frequency), 'w') as file:
            # Remove duplicates by converting to set and back in case of
            # malicious WordNet.
            file.write('\n'.join(list(set(words))))

        return words


def generate_phrase_1():
    selections = [VERBS, ADJECTIVES, NOUNS, ADVERBS, TRANSITIVE_VERBS, VERBS, ADJECTIVES, NOUNS]
    entropy = sum([log(len(item), 2) for item in selections])
    conjugations = ['part', None, None,
                    None, [random_item_from_list([PAST, PRESENT])],
                    'part', None, None]
    entropy += 1
    print('%.2f bits of entropy' % entropy)
    sub_list = [random_item_from_list(item) for item in selections]
    for idx, word in enumerate(sub_list):
        if conjugations[idx]:
            sub_list[idx] = conjugate(word, *conjugations[idx])

    return ('the %s %s %s %s %s the %s %s %s' % tuple(sub_list)).replace('_', ' ')


def generate_phrase_2():
    '''Return a phrase and its entropy (in bits) of the form
       (# adj noun) (adverb verb) (adjective noun punctuation)

    E.g.,
       17 MODERATE TRAYS At once live outed wORTH bOSSES
    '''
    selections = [ADJECTIVES, NOUNS,
                  ADVERBS, TRANSITIVE_VERBS,
                  ADJECTIVES, NOUNS, TERMINAL_PUNCTUATION]
    entropy = sum([log(len(item), 2) for item in selections])
    conjugations = [None, None,
                    None, [random_item_from_list([PAST, PRESENT]), 3, PLURAL],
                    None, None,
                    None]
    sub_list = [random_item_from_list(item) for item in selections]
    for idx, word in enumerate(sub_list):
        if conjugations[idx]:
            sub_list[idx] = conjugate(word, *conjugations[idx])
    entropy += 1

    sub_list[1] = pluralize(sub_list[1])
    sub_list[5] = pluralize(sub_list[5])

    entropy += log(997, 2)

    for idx, item in enumerate(sub_list):
        rnd = randint(4)
        if rnd == 1:
            sub_list[idx] = item.capitalize()
        if rnd == 2:
            sub_list[idx] = item.upper()
        if rnd == 3:
            sub_list[idx] = item[0] + item[1:].upper()

        entropy += 2

    phrase = ('%i %s %s %s %s %s %s%s' % tuple([randint(997) + 2] + sub_list)).replace('_', ' ')

    # Insert a random symbol into the sentence
    insert_point = randint(len(phrase) + 1)
    entropy += log(len(phrase) + 1, 2) + log(len(SYMBOLS), 2)
    phrase = phrase[:insert_point] + random_item_from_list(SYMBOLS) + phrase[insert_point:]

    insert_point = randint(len(phrase) + 1)
    entropy += log(len(phrase) + 1, 2) + log(len(SYMBOLS), 2)
    phrase = phrase[:insert_point] + random_item_from_list(SYMBOLS) + phrase[insert_point:]

    return phrase, entropy


# Ensure WordNet is installed.
try:
    wordnet.lemmas('A')
except:
    nltk.download('wordnet')

TRANSITIVE_VERBS = trans_verb_list()
VERBS = words_of_type('VERB')
NOUNS = words_of_type('NOUN', 6)
ADJECTIVES = words_of_type('ADJ')
ADVERBS = words_of_type('ADV')
TERMINAL_PUNCTUATION = ['.', '...', '!', '?']
SYMBOLS = list('~!@#$%^&*()_+-=[]\\{}|;:<>/')
