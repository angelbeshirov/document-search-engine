import configparser
import regex as re
    
class TextProcessor:

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
        return re.sub('[Сс][ГгТт][Рр]\.[\s]*[1-9][0-9]*[\.]*', '', file)

    def process(self, text):
        text = self.clear_pages(text)
        text = self.clear_hyphens(text)

        return text
