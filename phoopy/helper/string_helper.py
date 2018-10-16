# -*- coding: utf-8 -*-

import re
import string
from collections import Counter


class StringHelper(object):
    @staticmethod
    def snake_case(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def remove_suffix(name, suffix):
        return re.sub('(.)({})'.format(suffix), r'\1', name)

    @staticmethod
    def filter_printable_characters(text):
        accents = 'áéíóúÁÉÍÓÚ'
        extras = 'ñÑç'
        brasilian = 'ãàâçêíõôü'
        printable = accents + extras + string.printable + brasilian
        return ''.join(filter(lambda x: x in printable, text))

    @staticmethod
    def is_valid_word(word, stopwords):
        for stopword in stopwords:
            if word.lower() != stopword.lower():
                continue
            return False

        without_punctuation = word.translate(str.maketrans('', '', string.punctuation)).strip()

        if len(without_punctuation) == 0:
            return False

        return True

    @staticmethod
    def get_most_used_words(words, stopwords):
        valid_words = [word.lower() for word in words if StringHelper.is_valid_word(word, stopwords)]
        return dict(Counter(valid_words).most_common(5))
