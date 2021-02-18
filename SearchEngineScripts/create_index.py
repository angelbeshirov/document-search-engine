from elasticsearch import Elasticsearch
import os
import glob
import PyPDF2
import pandas as pd
import codecs   
from fpdf import FPDF
import pycpdf
import argparse

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