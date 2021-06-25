from elasticsearch import Elasticsearch
from config import ConfigManager
from preprocess import TextProcessor
from nltk.tokenize import WordPunctTokenizer
from collections import Counter

import os
import glob
import codecs
from fpdf import FPDF
import pycpdf
import pickle

class Extractor:

    def __init__(self, config = ConfigManager()):
        self.tokenizer = WordPunctTokenizer()
        self.clada_dictionary = set(line.strip()\
            for line in open(config.get_dictionary(), encoding = 'utf-16', mode = "r"))
    
    def extract(self, files):
        """
        Extracts the contentes of the pdf files, clears it up
        and puts it in a single txt file for further preprocessing.
        """
        processor = TextProcessor()
        content = ''
        raw_content = ''
        
        for file in files:
            print("Extracting document {}".format(file))
            pdf_file_object = open(file, "rb")
            pdf_reader = pycpdf.PDF(pdf_file_object.read())
            
            n_pages = len(pdf_reader.pages)
            
            for i in range(n_pages):
                page_object = pdf_reader.pages[i]
                this_text = page_object.text.translate(pycpdf.unicode_translations)
                this_text = processor.process(this_text)
                if this_text:
                    raw_content += this_text
                    content += (file + ',' + str(i + 1) + ',' + this_text + os.linesep)

        f = open("dictionary/corpus.txt", "w+")
        f.write(content)
        f.close()

        if not os.path.isfile("dictionary/count_dictionary.pickle"):
            tokens = self.tokens(raw_content)
            counter = Counter(tokens)

            with open('dictionary/count_dictionary.pickle', 'wb') as outputfile:
                pickle.dump(counter, outputfile)

    def tokens(self, text): 
        tokens = self.tokenizer.tokenize(text)
        filtered = filter(lambda token: token in self.clada_dictionary, tokens)
        return filtered

def get_files(root_path):
    """
    Recursively traverses root_path directory 
    to find all files with pdf extension and returns
    them as array for indexing.
    """
    all_files= []

    print(os.walk(root_path))
    for root, dirs, files in os.walk(root_path):
        for file in files:
            print(file)
            if file.endswith(".pdf"):
                all_files.append((os.path.join(root, file)))

    return all_files

def main():
    config = ConfigManager()
    extractor = Extractor()
    
    print("Directory path for extraction {}", config.get_path())
    files = get_files(config.get_path())

    for file in files:
        print(os.path.abspath(file))

    extractor.extract(files)
    
if __name__ == '__main__':
    main()
