#standard imports
import os
import pandas as pd
import matplotlib.pyplot as plt

# natural language processing: n-gram ranking
import re
import unicodedata
import nltk
from nltk.corpus import stopwords

# read and store all keywords and stopwords
keywords_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Read_Files", "keywords.txt"))
with open(keywords_path) as file:
    keywords = [line.strip().lower() for line in file]
stopwords = nltk.corpus.stopwords.words('english')
stopwords_with_keywords = stopwords + keywords

# function to cleanup text and find words in it
def extract_words_from_text(text, keywords_excluded=False):
    """
    Function to clean up the passed text.\n
    All words that are not designated as a stop word are lemmatized afte encoding and basic regex parsing is performed.\n
    \n
    Parameters:
    text - Text to be worked with
    keywords_excluded - 'True' if keywords are to be treaded as stopwords
    """

    # lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()

    # text cleaning
    text = (unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore').lower())
    words = re.sub(r'[^\w\s]', '', text).split()

    # word list
    if keywords_excluded:
        return [wnl.lemmatize(word) for word in words if word not in stopwords_with_keywords]
    else:
        return [wnl.lemmatize(word) for word in words if word not in stopwords]

# function to extract plots from given dataframe
def extract_plots(df, plot_save_path, keywords_excluded=False, max_n=3, max_rows=10):
    """
    Plots n-grams from given df["Blog Title"] for all n = {1, 2, ..., max_n}, excluding keywords if required.\n
    \n
    Parameters:\n
    df - Pandas DataFrame to be used
    plot_save_path - Directory path where plots will be saved
    keywords_excluded - 'True' if keywords are to be treaded as stopwords
    max_n - Maximum n value while finding n-grams
    max_rows - Number of results to show
    """

    # word list from titles
    words = extract_words_from_text(text="".join(str(df["Blog Title"].tolist())), keywords_excluded=keywords_excluded)

    # saving plots for all n
    for curr_n in range(1, max_n+1):\
        # generating plot
        series = (pd.Series(nltk.ngrams(words, curr_n)).value_counts())[:max_rows]
        series.sort_values().plot.barh(width=.8, figsize=(20, 15))

        # plot labels
        if keywords_excluded:
            plt.title(f'{max_rows} Most Frequently Occuring {curr_n}-grams, Excluding Keywords')
            plot_save_name = os.path.abspath(os.path.join(plot_save_path, f"n{curr_n}_keywords_excluded.png"))
        else:
            plt.title(f'{max_rows} Most Frequently Occuring {curr_n}-grams')
            plot_save_name = os.path.abspath(os.path.join(plot_save_path, f"n{curr_n}.png"))
        plt.ylabel(f'{curr_n}-gram')
        plt.xlabel('No. of Occurances')

        # saving plot
        plt.savefig(plot_save_name)
        plt.clf()

# main process
def extract_all_plots(max_n=3, max_rows=10):
    print("Extracting all plots...")
    
    # read all keyword containing data
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cumulative_data_with_keyword_count.csv"))
    dataframe = pd.read_csv(csv_path)
    dataframe = dataframe.loc[dataframe["keyword_count"] > 0]

    # save path for plots
    save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Ngram_Histogram_Plots"))

    # plot with and without keywords
    extract_plots(df=dataframe, plot_save_path=save_path, keywords_excluded=False, max_n=max_n, max_rows=max_rows)
    extract_plots(df=dataframe, plot_save_path=save_path, keywords_excluded=True, max_n=max_n, max_rows=max_rows)

if __name__ == "__main__":
    print("Processing...")

    # maximum n value for generating ngrams
    maximum_n_value = 3
    # how many ngrams to show
    max_rows_in_output = 20
    
    extract_all_plots(max_n=maximum_n_value, max_rows=max_rows_in_output)
    print("Finished.")
