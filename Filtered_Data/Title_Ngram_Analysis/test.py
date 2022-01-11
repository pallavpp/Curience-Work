# natural language processing: n-gram ranking
import os
import re
import unicodedata
import nltk
from nltk.corpus import stopwords

stopwords = nltk.corpus.stopwords.words('english')
print(stopwords)
print(type(stopwords))
print(type(stopwords[0]))

# read and store all keywords and stopwords
keywords_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Read_Files", "keywords.txt"))
with open(keywords_path) as file:
    keywords = [line.strip().lower() for line in file]
print(keywords)
print(type(keywords))
print(type(keywords[0]))

stopwords_with_keywords = stopwords + keywords
print(stopwords_with_keywords)
print(type(stopwords_with_keywords))
print(type(stopwords_with_keywords[0]))
