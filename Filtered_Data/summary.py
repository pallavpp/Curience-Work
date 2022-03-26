# standard imports
import re
import requests
import numpy as np
import unicodedata
import pandas as pd
import networkx as nx
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity

# custom imports
import os
import sys
modules_path  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
if modules_path not in sys.path:
    sys.path.insert(1, modules_path)
import SaveDataAsCSV

# current file path
curr_path = os.path.abspath(__file__)

# read all stopwords
stopwords_path = os.path.abspath(os.path.join(curr_path, "../..", "Read_Files", "stopwords_cleaned.txt"))
with open(stopwords_path) as file:
    stopwords = [line.strip().lower() for line in file]

# read all word embeddings
word_embeddings = {}
file_path = os.path.abspath(os.path.join(curr_path, "../..", "Read_Files/glove_embeddings", "glove.6B.100d.txt"))
f = open(file_path, encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()

# function to clean page text
def clean_sentence(text):
    # text cleaning
    text = (unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore').lower())
    text = text.replace("/", " ")
    text = text.replace("-", " ")
    words = re.sub(r'[^\w\s]', '', text).split()

    return " ".join([word for word in words if word not in stopwords])

# function to get all page content from html response
def get_page_text(html_response):
    # getting page content
    html_text = html_response.text
    soup = BeautifulSoup(html_text, "lxml")

    # various sources of text
    para_text = [element.text.strip() for element in soup.find_all("p")]
    header_text = [element.text.strip() for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
    span_text = [element.text.strip() for element in soup.find_all("span")]
    
    return " ".join(para_text), " ".join(header_text), " ".join(span_text)

# function to get page text for all blogs
def get_text(df):
    para_text = []
    header_text = []
    span_text = []

    for blog_link in df["Blog Link"]:
        # getting page response
        html_response = requests.get(blog_link)
        if(html_response.status_code != 200):
            para_text.append("")
            header_text.append("")
            span_text.append("")
        else:
            ret = get_page_text(html_response)
            para_text.append(ret[0])
            header_text.append(ret[1])
            span_text.append(ret[2])
    
    return para_text, header_text, span_text

# main process
def main(summary_size):
    # blog data
    df = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "final_data.csv")))
    
    # add columns
    ret = get_text(df)
    df["Para Text"] = ret[0]
    df["Header Text"] = ret[1]
    df["Span Text"] = ret[2]
    
    # saving data as csv
    SaveDataAsCSV.df_to_csv_in_currdir(dataframe=df, caller_path=__file__, csv_filename="final_data.csv")

if __name__ == "__main__":
    print("Processing...")

    # summary_size
    summary_size = 10
    main(summary_size)

    print("Finished.")
