from elasticsearch import Elasticsearch
from config import ConfigManager
from preprocess import TextProcessor
from corrector import Corrector

import os
import glob
import pandas as pd
import codecs   
from fpdf import FPDF
import pycpdf
    
def extract_and_index(files, config_manager):
    """
    Extracts the contentes of the pdf files, clears it up
    and passes it to Elastic for indexing.
    """
    es = Elasticsearch([config_manager.get_address()])
    processor = TextProcessor()
    
    for file in files:
        print("Indexing document {}".format(file))
        pdf_file_object = open(file, "rb")
        pdf_reader = pycpdf.PDF(pdf_file_object.read())
        
        n_pages = len(pdf_reader.pages)
        
        document_content = ''
        for i in range(n_pages):
            page_object = pdf_reader.pages[i]
            this_text = page_object.text.translate(pycpdf.unicode_translations)
            document_content += this_text
        
        document_content = processor.process(document_content)
        print(document_content)

        body = {}

        # Change accordingly
        temp = os.path.abspath(file).split('/')[-3:]
        path = "/home/ec2-user/" + '/'.join(temp)
        body["path"] = path #os.path.abspath(file)
        body["content"] = document_content

        #es.index(index = 'library_index', body = body)

def get_files_to_index(root_path):
    """
    Recursively traverses root_path directory 
    to find all files with pdf extension and returns
    them as array for indexing.
    """
    files_to_index = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".pdf"):
                files_to_index.append((os.path.join(root, file)))

    return files_to_index

def main():
    config = ConfigManager()

    files = get_files_to_index(config.get_path())

    for file in files:
        print(os.path.abspath(file))

    # extract_and_index(files, config)
    corrector = Corrector()
    
if __name__ == '__main__':
    main()
