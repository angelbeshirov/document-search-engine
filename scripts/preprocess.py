import configparser
import regex as re
from config import ConfigManager


class TextProcessor:

    def __init__(self, config=ConfigManager()):
        self.clada_dictionary = set(line.strip() \
                                    for line in open(config.get_dictionary(), encoding='utf-16', mode="r"))

    def clear_hyphens(self, text):
        """
        Clear all hyphens which are a result from word
        separation on 2 different lines.
        """
        """ по- красив -> по-красив """
        text = re.sub('(по-)([\s]*[\r\n]*)([а-яА-Я])', '\\1\\3', text)
        """ най- красив -> най-красив """
        text = re.sub('(най-)([\s]*[\r\n]*)([а-яА-Я])', '\\1\\3', text)
        """ стру- ва -> струва """
        return re.sub('([а-яА-Я])(-[\s]+)([а-яА-Я])', '\\1\\3', text)

    def clear_pages(self, file):
        """
        Clear up the pages.
        """
        # изтриване на част от страниците
        file = re.sub('-[\s][0-9]+[\s]-[\s]*', '', file)
        file = re.sub('[Сс][ГгТт][Рр][\.\-,][\s]*[-]*([1-9][0-9]*)?[-]?([1-9][0-9]*)?[\.\-,]*', '', file)
        return re.sub('[\s]+', ' ', file)

    def correct_words_with_hyphens(self, text):
        regex = re.compile('\s+')
        words = regex.split(text)

        preprocessed_text = text
        for i, word in enumerate(words):
            if "-" in word and i < len(words) - 1:
                next_word = words[i + 1]

                semi_light_word = word + next_word
                merged_word = word.replace("-", "") + next_word

                original_seq = word + " " + next_word
                if semi_light_word in self.clada_dictionary:
                    preprocessed_text = re.sub(original_seq, semi_light_word, preprocessed_text)
                elif merged_word in self.clada_dictionary:
                    preprocessed_text = re.sub(original_seq, merged_word, preprocessed_text)

        return preprocessed_text

    def process(self, text):
        text = self.clear_pages(text)
        text = self.clear_hyphens(text)
        text = self.correct_words_with_hyphens(text)

        return text
