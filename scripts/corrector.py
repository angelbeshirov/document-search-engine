from nltk.tokenize import WordPunctTokenizer

import json
import Levenshtein
import pickle
import csv
import re
import os
from config import ConfigManager


class Corrector:

    def __init__(self, config = ConfigManager()):
        self.tokenizer = WordPunctTokenizer() # Tokenizer 
        self.clada_dictionary = set(line.strip()\
            for line in open(config.get_dictionary(), encoding = 'utf-16', mode = "r"))
            
        self.learned_dictionary = dict()

        if os.path.isfile("dictionary/learned_dictionary.pickle"):
            with open('dictionary/learned_dictionary.pickle', "rb") as learned_dict_file:
                self.learned_dictionary = pickle.load(learned_dict_file)

        with open('dictionary/count_dictionary.pickle', "rb") as input_file:
            self.count_dictionary = pickle.load(input_file)

        self.total = sum(self.count_dictionary.values())

        header = ['Файл', 'Страница', 'Позиция', 'Контекст', 'Сгрешен OCR' , 'Предложения за поправка', 'Поправен OCR']

        f = open('suggestions.csv', 'w', encoding='UTF16')
        self.writer = csv.writer(f)
        self.writer.writerow(header)

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

                if token in self.learned_dictionary:
                    suggestions.insert(0, self.learned_dictionary[token])
                    
                if len(suggestions) > 0:
                    sorted_suggestions = sorted(suggestions, key=lambda token: self.probability(token, self.total))[:5]
                    
                    suggestions = ' | '.join(sorted_suggestions).strip()
                    self.writer.writerow([entry_doc, entry_page, i, self.get_context(i, tokenized_text), token, suggestions, ''])
            else:
                self.writer.writerow([entry_doc, entry_page, i, self.get_context(i, tokenized_text), token, corrected_token, ''])
                tokenized_text[i] = corrected_token

    def get_context(self, i, tokenized_text):
        cnt = 1
        words = 0
        punctuation=',;.!?-'
        context = []

        while words < 2 and i - cnt >= 0:
            context.insert(0, tokenized_text[i - cnt])

            if tokenized_text[i - cnt].strip() not in punctuation:
                words += 1
            cnt += 1

        context.append(tokenized_text[i])
        words = 0
        cnt = 1
        while words < 2 and i + cnt < len(tokenized_text):
            context.append(tokenized_text[i + cnt])

            if tokenized_text[i + cnt] not in punctuation:
                words += 1
            cnt += 1

        return self.join_tokenized_text(context)

    def autocorrect(self, token):
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

    def probability(self, word, total):
        """Probability of `word`."""

        return self.count_dictionary[word] / total

    def edits1(self, word):
        """All edits that are one edit away from `word`."""

        letters    = 'абвгдежзийклмнопрстуфхцчшщъьюяѫѣꙝѧωѝѹ'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        """All edits that are two edits away from `word`."""
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    def known(self, words):
        return set(w for w in words if w in self.clada_dictionary)

    def candidates_edits1(self, word):
        return list(self.known(self.edits1(word)))

    def candidates_edits2(self, word):
        return list(self.known(self.edits2(word)))


    def join_tokenized_text(self, tokenized_text):
        '''
        Join tokenized text.

        A simple join() cannot be used as this would treat alphanumeric tokens
        and punctuation the same. join_punctuation concatenates defined
        punctuation directly to previous token. Afterwards, a standard join()
        is applied.
        '''
        def join_punctuation(tokenized_text, char=',;.!?'):
            '''
            '''
            tokenized_text = iter(tokenized_text)
            current_item = next(tokenized_text)

            for item in tokenized_text:
                if item in char:
                    current_item += item

                    if item == '-':
                        current_item += next(tokenized_text)
                else:
                    yield current_item
                    current_item = item
            yield current_item

        return ' '.join(join_punctuation(tokenized_text))