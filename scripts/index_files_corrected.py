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
    
def extract_and_index(docs, config_manager):
    """
    Extracts the contentes of the pdf files, clears it up
    and passes it to Elastic for indexing.
    """
    es = Elasticsearch([config_manager.get_address()])
    
    for file_name in docs:
        print("Indexing document " + docs[file_name])

        body = {}

        # Change accordingly
        temp = os.path.abspath(file_name).split('/')[-3:]
        path = "/home/ec2-user/" + '/'.join(temp)
        body["path"] = path #os.path.abspath(file)
        body["content"] = docs[file_name]

        es.index(index = 'library_index', body = body)

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

def group_corpus(entries):
    grouped = {}

    for entry in entries:
        if entry['doc'] in grouped:
            grouped[entry['doc']] += entry['content']
        else:
            grouped[entry['doc']] = entry['content']

    return grouped

def main():
    config_manager = ConfigManager()

    entries = load_corpus()
    grouped = group_corpus(entries)

    print(grouped)
    extract_and_index(grouped, config_manager)
    
if __name__ == '__main__':
    main()
