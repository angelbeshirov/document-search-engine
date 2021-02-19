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
    es = Elasticsearch()

    es.indices.create('library_index', body = {
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
            "properties": {
                "content": {
                    "type": "text",
                    "index_options": "offsets"
                }
            }
        }
    })

    print("Index created successfully.")

if __name__ == '__main__':
    main()
