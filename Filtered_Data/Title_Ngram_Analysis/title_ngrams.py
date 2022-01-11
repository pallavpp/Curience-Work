#standard imports
import pandas as pd
import matplotlib.pyplot as plt

# natural language processing: n-gram ranking
import re
import unicodedata
import nltk
from nltk.corpus import stopwords

# custom imports
import os
import sys
modules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Modules"))
if modules_path not in sys.path:
    sys.path.insert(1, modules_path)
import SaveDataAsCSV

# read and store all keywords and stopwords
keywords_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Read_Files", "keywords.txt"))
with open(keywords_path) as file:
    keywords = [line.strip().lower() for line in file]
stopwords = nltk.corpus.stopwords.words('english')
stopwords_with_keywords = stopwords + keywords

def extract_words_from_titles(text, keywords_excluded=False):
    """
    A simple function to clean up the data. All the words that
    are not designated as a stop word is then lemmatized after
    encoding and basic regex parsing are performed.
    """
    wnl = nltk.stem.WordNetLemmatizer()
    text = (unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore').lower())
    words = re.sub(r'[^\w\s]', '', text).split()
    if keywords_excluded:
        return [wnl.lemmatize(word) for word in words if word not in stopwords_with_keywords]
    else:
        return [wnl.lemmatize(word) for word in words if word not in stopwords]

def extract_plots(df, keywords_excluded=False, max_n=3, max_rows=10):
    plots = []
    words = extract_words_from_titles(text="".join(str(df['Blog Title'].tolist())), keywords_excluded=keywords_excluded)

    for curr_n in range(1, max_n+1):
        series = (pd.Series(nltk.ngrams(words, curr_n)).value_counts())[:max_rows]
        series.sort_values().plot.barh(width=.8, figsize=(20, 16))
        if keywords_excluded:
            plt.title(f'{max_rows} Most Frequently Occuring {curr_n}-grams, excluding keywords')
        else:
            plt.title(f'{max_rows} Most Frequently Occuring {curr_n}-grams')
        plt.ylabel(f'{curr_n}-gram')
        plt.xlabel('# of Occurances')
        plt.show()
    return plots

# main process
def extract_all_plots(max_n=3, max_rows=10):
    print("Extracting all plots...")
    
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "cumulative_data_with_keyword_count.csv"))
    dataframe = pd.read_csv(csv_path)
    # plots = extract_plots(df=dataframe, keywords_excluded=False, max_n=max_n, max_rows=max_rows)
    # for curr_plot in plots:
    #     pass
    plots = extract_plots(df=dataframe, keywords_excluded=True, max_n=max_n, max_rows=max_rows)
    for curr_plot in plots:
        pass

    # keyword_containing_data_csv_path = ""
    # best_data_csv_path = ""

    print("All plots saved.")

if __name__ == "__main__":
    print("Processing...")

    # maximum n value for generating ngrams
    maximum_n_value = 5

    # how many ngrams to show
    max_rows_in_output = 20
    
    extract_all_plots(max_n=maximum_n_value, max_rows=max_rows_in_output)
    print("Finished.")
