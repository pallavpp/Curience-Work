# Curience-Work
Pallav and Alokeveer's Work.\
The documentation is uploaded in PDF format. To view the documentation as a Google Doc, click [here](https://docs.google.com/document/d/1RS7Ipab4UIDa-klV3QauxywEPghJm06_RBgKH31ZHZQ/edit?usp=sharing).

## Workflow
1. Write scraping scripts in the _Scripts_ folder. Save the scraped data in _Data_ folder
2. Run _Filtered_Data/cumulative_data_with_keyword_count.py_
3. Run _Filtered_Data/title_ngrams.py_ to check if any related keyword is not missed
4. Run _Filtered_Data/final_data.py_ to get shortlisted blogs
5. Run _Filtered_Data/summary.py_ to store all blog text in _final_data.csv_
6. Run _Filtered_Data/recall.py_ to get recall score
7. Test various analytic techniques in the _Analytics_ folder. Save outputs in the _Outputs_ folder

## Info
- Scraping scripts are present in `Scripts` folder.
    - Scraped data will be saved in CSV format in `Data` folder.
    - Before running scripts that use selenium, user will have to update _driver path_ in script.
    - For all scraping scripts, choose column names from the following list only: ["Blog Title", "Blog Date", "Blog Catchphrase", "Blog Category", "Blog Link", "Author Name", "Author Profile Link", "Thumbnail Link", "Thumbnail Credit"]. ***If you decide to include any new column name not listed here, update the above list so others know to use it in the future. If not done, filtered data may contain redundant columns.***
- Custom modules are present in `Modules` folder. Add following code to scripts to import custom modules:
    ```
    import os
    import sys
    modules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
    if modules_path not in sys.path:
        sys.path.insert(1, modules_path)
    ```
- Files containing reading data are present in `Read_Files` folder.
    - ***Each line in Read_Files/keywords.txt is treated as a keyword, used for the naive sorting.***
    - _Read_Files/stopwords.txt_ contains a stopword list and _Read_Files/stopwords_cleaned.txt_ contains the same words, but in regex cleaned form.
- `Filtered_Data` folder contains filtering scripts and sorted, cumulated and filtered data.
    - _Filtered_Data/cumulative_data_with_keyword_count.py_ reads all CSV files from `Data` folder and filters them based on keywords read from _Read_Files/keywords.txt_.
    - _Filtered_Data/final_data.py_ sorts and return top results in _cumulative_data_with_keyword_count.csv_. If required, user will have to update _max rows in output_ in the script. Following scoring criteria is used:
        - Start with an initial score of 0
        - If some year is present in the Blog Title - remove if >= 2010 and <= 2021. If 2022 is present, the blog can't be removed in future steps
        - If Blog Date or Blog/Thumbnail Link contains year < 2021 - remove if permitted
        - +1 for each unique keyword present in the title
        - +1 additionally for ("summer" or "spring" or "2022") presence in title
        - +1 additionally for "2022" presence in the blog link
    - _Filtered_Data/title_ngrams.py_ geneates n-grams based on blog titles for all positively scored data in _cumulative_data_with_keyword_count.csv_. Plots are saved in `Ngram_Histogram_Plots` folder.
    - _Filtered_Data/divide_csv.py_ divides _final_data.csv_ in two parts and saves in `Analytics` folder for document analytics.
    - _Filtered_Data/recall.py_ calculates the recall score for blog links in _Filtered_Data/cumulative_data_with_keyword_count.csv_ based on links present in _Read_Files/fashion_intern_forecasting_website_list.csv_
    - _Filtered_Data/summary.py_ goes through all blogs in _Filtered_Data/final_data.py_, and appends the html text obtained in columns. This allows for effecient access to blog text.
- `Analytics` folder contains document analytics.
    - All outputs are saved in _Outputs_ folder.
    - Execution of _Analytics/Pallav/textrank/vogue_test.ipynb_ requires use of GloVe embeddings. Heads Up - the size of these word embeddings is 822 MB. Extract all files and place them inside _Read_Files/glove_embeddings/_. Files can be downloaded [here](https://nlp.stanford.edu/data/glove.6B.zip).

## All Requirements
- [Selenium](https://pypi.org/project/selenium/)
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)
- [pandas](https://pypi.org/project/pandas/)
- [Matplotlib](https://pypi.org/project/matplotlib/)
- [NLTK](https://pypi.org/project/nltk/)
- [Requests](https://pypi.org/project/requests/)
- [lxml](https://pypi.org/project/lxml/)
- [dataclasses](https://pypi.org/project/dataclasses/)
