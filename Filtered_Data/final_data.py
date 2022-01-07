# standard imports
import glob
from typing import final
import pandas as pd

# custom imports
import os
import sys
modules_path  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
if modules_path not in sys.path:
    sys.path.insert(1, modules_path)
import SaveDataAsCSV

# read and store all keywords in lowercase
keywords_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Read_Files", "keywords.txt"))
with open(keywords_path) as file:
    keywords = [line.strip().lower() for line in file]

# function to find if any keyword is present in blog title
def get_score(blog_title_lowercase):
    score = 0
    for keyword in keywords:
        if keyword in blog_title_lowercase:
            score += 1
    return score

# main process
def extract(max_rows):
    final_df = pd.DataFrame()
    data_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Data"))

    for path in glob.glob(data_folder_path + "\*.csv"):
        curr_df = pd.read_csv(path)
        score_values = curr_df.apply(lambda x: get_score(x["Blog Title"].lower()), axis=1)
        curr_df["row_score"] = score_values
        final_df = pd.concat([final_df, curr_df], ignore_index=True)

    # dropping rows conatining duplicate blog links
    final_df.drop_duplicates(subset=["Blog Link"], inplace=True, ignore_index=True)

    # replacing NaN with empty string
    final_df.fillna("", inplace=True)

    # sort and save cumulative data
    final_df.sort_values(by="row_score", ascending=False, inplace=True)
    SaveDataAsCSV.df_to_csv_in_currdir(dataframe=final_df, caller_path=__file__, csv_filename="cumulative_data_with_score.csv")
    final_df.drop("row_score", axis=1, inplace=True)

    # saving combined data as csv
    if final_df.shape[0] > max_rows:
        final_df = final_df.loc[:max_rows]
    SaveDataAsCSV.df_to_csv_in_currdir(dataframe=final_df, caller_path=__file__)

if __name__ == "__main__":
    print("Processing...")

    # maximum number of rows in output
    max_rows_in_output = 100
    
    extract(max_rows=max_rows_in_output)
    print("Finished.")
