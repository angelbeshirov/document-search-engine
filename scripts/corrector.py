from nltk.tokenize import WordPunctTokenizer

import json
import Levenshtein
import pickle
import csv
import re
from config import ConfigManager


class Corrector:  # 'dictionary/CLADABG-MODEL.txt'

    def __init__(self, config=ConfigManager()):
        self.tokenizer = WordPunctTokenizer()  # Tokenizer
        self.clada_dictionary = set(line.strip() \
                                    for line in open(config.get_dictionary(), encoding='utf-16', mode="r"))
        # for line in open('dictionary/all-cyrillic.txt', encoding = 'utf-8', mode = "r"))

        # self.learned_dictionary = self.load_learned_dictionary('dictionary/learned_dictionary.json')

        with open('dictionary/count_dictionary.pickle', "rb") as input_file:
            self.count_dictionary = pickle.load(input_file)

        self.total = sum(self.count_dictionary.values())

        header = ['Файл', 'Страница', 'Позиция', 'Сгрешен OCR', 'Предложения за поправка', 'Поправен OCR']

        f = open('suggestions.csv', 'w', encoding='UTF16')
        f1 = open('suggestions1edit.csv', 'w', encoding='UTF16')
        self.writer = csv.writer(f)
        self.writer1 = csv.writer(f1)
        self.writer.writerow(header)
        self.writer1.writerow(header)

    def correct(self, entry):
        """
        Data is a single entry in the format docId,page,content
        """
        entry_doc = entry['doc']
        entry_page = entry['page']
        entry_text = entry['content']

        print("Processing doc {}, page {}".format(entry['doc'], entry['page']))

        tokenized_text = self.tokenize_text(entry_text)  # Tokenize the text

        for i, token in enumerate(tokenized_text):
            if self.check_clada_dict(token):  # Don't want to correct tokens which are in CLADA dictionary
                continue
            elif self.token_not_eligible(token):
                continue

            corrected_token = self.autocorrect(token)

            if corrected_token is None:
                # Get suggestions of edit distance 2, sort them on probability and get the top 5
                suggestions = self.candidates_edits2(token)
                if len(suggestions) > 0:
                    sorted_suggestions = sorted(suggestions, key=lambda token: self.probability(token, self.total))[:5]

                    suggestions = '|'.join(sorted_suggestions)
                    self.writer.writerow([entry_doc, entry_page, i, token, suggestions, ''])
            else:
                self.writer1.writerow([entry_doc, entry_page, i, token, corrected_token, ''])
                tokenized_text[i] = corrected_token

    def autocorrect(self, token):
        # if self.is_in_learned_dict(token):
        #     return self.learned_dict[token]

        candidates = self.candidates_edits1(token)

        if len(candidates) > 0:
            top_candidate = sorted(candidates, key=lambda candidate: self.probability(candidate, self.total))[:1]

            return top_candidate[0]

        return None

    def token_not_eligible(self, token):
        return re.search('[а-яѫѣꙝѧωѝѹ]', token.lower()) is None

    def tokenize_text(self, text):
        """
        Tokenize text.

        The WordPunctTokenizer separates punctuation from alphanumeric tokens.
        """
        return self.tokenizer.tokenize(text)

    def check_clada_dict(self, token):
        return True if token in self.clada_dictionary else False

    def check_learned_dict(self, token):
        return True if token in self.learned_dict else False

    def load_learned_dictionary(self, path):
        with open(path) as f:
            data = f.read()

        return json.loads(data)

    def calculate_levenshtein_distance(self, token, alt_spellings):
        '''Calculate Levenshtein distance of alternative spellings to error.'''
        distances = {}
        for spelling in alt_spellings:
            distances[spelling] = Levenshtein.distance(token, spelling)
        return distances

    def probability(self, word, total):
        """Probability of `word`."""

        return self.count_dictionary[word] / total

    def edits1(self, word):
        """All edits that are one edit away from `word`."""

        letters = 'абвгдежзийклмнопрстуфхцчшщъьюяѫѣꙝѧωѝѹ'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        """All edits that are two edits away from `word`."""
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    def known(self, words):
        return set(w for w in words if w in self.clada_dictionary)

    def candidates_edits1(self, word):
        return set(self.known(self.edits1(word)))

    def candidates_edits2(self, word):
        return set(self.known(self.edits2(word)))
