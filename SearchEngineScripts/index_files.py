from elasticsearch import Elasticsearch
import os
import glob
import PyPDF2
import pandas as pd
import codecs   
from fpdf import FPDF
import pycpdf
import argparse
import regex as re

def clear_hyphens(file):
    """
    Clear all hyphens which are a result from word
    separation on 2 different lines.
    """
    # по- красив -> по-красив
    file = re.sub('(по-)([\s]*[\r\n]*)([а-яА-Я])', '\\1\\3', file)
    # най- красив -> най-красив
    file = re.sub('(най-)([\s]*[\r\n]*)([а-яА-Я])', '\\1\\3', file)
    # стру- ва -> струва
    return re.sub('([а-яА-Я])(-[\s]+)([а-яА-Я])', '\\1\\3', file)

def clean(file):
    """
    Clear up the pages.
    """
    # изтриване на част от страниците
    file = re.sub('-[\s][0-9]+[\s]-[\s]*', '', file)
    file = clear_hyphens(file)
    return file
    
def extract_and_index(files):
    """
    Extracts the contentes of the pdf files, clears it up
    and passes it to Elastic for indexing.
    """
    es = Elasticsearch()
    
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
        
        document_content = clean(document_content)

        body = {}
        body["path"] = os.path.abspath(file)
        body["content"] = document_content

        es.index(index = 'library_index', body = body)

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
    # parameters used for starting this class from shell scripts and executing different flows with different paremeters
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--path", type=str, default=".", help="Path to the directory with the files to index.")
    args = parser.parse_args()

    path = args.path
    files = get_files_to_index(path)

    for file in files:
        print(os.path.abspath(file))

    extract_and_index(files)
    
if __name__ == '__main__':
    main()
