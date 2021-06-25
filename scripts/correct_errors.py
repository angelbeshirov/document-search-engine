from nltk.tokenize import WordPunctTokenizer
from csv import DictReader

import pickle
import os


def load_corpus():
    path_to_file = './dictionary/corpus.txt'
    f = open(path_to_file, encoding='utf-8', mode="r")

    entries = []
    while True:
        line = f.readline()

        if not line:
            break

        line = line.split(",")
        entry = {'doc': line[0], 'page': int(line[1]), 'content': ','.join(line[2:])}

        entries.append(entry)

    f.close()
    return entries


def join_tokenized_text(tokenized_text):
    """
    Join tokenized text.

    A simple join() cannot be used as this would treat alphanumeric tokens
    and punctuation the same. join_punctuation concatenates defined
    punctuation directly to previous token. Afterwards, a standard join()
    is applied.
    """

    def join_punctuation(tokenized_text, char=',;.!?-'):
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


class ErrorsCorrector:

    def __init__(self):
        self.tokenizer = WordPunctTokenizer()  # Tokenizer

        # Load corpus
        self.entries = load_corpus()

        # Load current dictionary
        input_file = open('dictionary/corrections_dictionary.pickle', 'rb')
        self.corrections_map = pickle.load(input_file)
        input_file.close()

        suggestions_fd = open('suggestions.csv', 'r', encoding='UTF16')
        self.reader = DictReader(suggestions_fd)

    def correct_with_suggestions(self):
        for row in self.reader:
            if row['Поправен OCR'] is not None and row['Поправен OCR'] != '':
                entry = next((x for x in self.entries if x['doc'] == row['Файл'] and x['page'] == int(row['Страница'])),
                             None)

                if entry is not None:
                    tokenized_text = self.tokenizer.tokenize(entry['content'])
                    for i, token in enumerate(tokenized_text):
                        if i == int(row['Позиция']):
                            tokenized_text[i] = row['Поправен OCR']
                            entry['content'] = join_tokenized_text(tokenized_text) + os.linesep

                    # append wrong right value to dictionary
                    self.corrections_map.append({row['Сгрешен OCR']: row['Поправен OCR']})

        # update content in the corpus
        self.update_corpus()

        # update corrections dictionary
        self.append_to_corrections_dictionary()

    def append_to_corrections_dictionary(self):
        outfile = open('dictionary/corrections_dictionary.pickle', 'wb')
        pickle.dump(self.corrections_map, outfile)
        outfile.close()

    def update_corpus(self):
        path_to_file = './dictionary/corpus.txt'
        f = open(path_to_file, encoding='utf-8', mode="w")

        for entry in self.entries:
            content = entry['doc'] + ',' + str(entry['page']) + ',' + entry['content']
            f.write(content)

        f.close()


def main():
    errors_corrector = ErrorsCorrector()
    errors_corrector.correct_with_suggestions()


if __name__ == '__main__':
    main()
