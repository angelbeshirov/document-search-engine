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

def clearHyphens(file):
    # по- красив -> по-красив
    file = re.sub('(по-)([\s]*[\r\n]*)([а-яА-Я])', '\\1\\3', file)
    # най- красив -> най-красив
    file = re.sub('(най-)([\s]*[\r\n]*)([а-яА-Я])', '\\1\\3', file)
    # стру- ва -> струва
    return re.sub('([а-яА-Я])(-[\s]+)([а-яА-Я])', '\\1\\3', file)

def clean(file):
    # изтриване на част от страниците
    file = re.sub('-[\s][0-9]+[\s]-[\s]*', '', file)
    file = clearHyphens(file)
    return file
    
def extractPdfFilesDocumentwise(files):
    loc = 1
    df = pd.DataFrame(columns = ("path", "content"))
    
    for file in files:
        print("Extracting document {}".format(loc))
        pdfFileObj = open(file, "rb")
        pdfReader = pycpdf.PDF(pdfFileObj.read())
        
        n_pages = len(pdfReader.pages)
        
        this_doc = ''
        for i in range(n_pages):
            pageObj = pdfReader.pages[i]
            this_text = pageObj.text.translate(pycpdf.unicode_translations)
            this_doc += this_text
        
        this_doc = clean(this_doc)
        df.loc[loc] = os.path.abspath(file), this_doc
        loc = loc + 1
        
    return df

def main():
    # parameters used for starting this class from shell scripts and executing different flows with different paremeters
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--path", type=str, default=".", help="Path to the directory with the files to index.")
    args = parser.parse_args()

    path = args.path
    os.chdir(path)
    files = glob.glob("*.*")

    for file in files:
        print(os.path.abspath(file))

    df = extractPdfFilesDocumentwise(files)
    es = Elasticsearch()

    column_names = df.columns
    for row in range(df.shape[0]):
        body = dict([(name, str(df.iloc[row][name])) for name in column_names])
        es.index(index = 'library_index', body = body)

if __name__ == '__main__':
    main()
