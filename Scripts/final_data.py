# standard imports
import glob
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
def filter_using_keywords(blog_title_lowercase):
    flag = False
    for keyword in keywords:
        if keyword in blog_title_lowercase:
            flag = True
            break
    return flag

# main process
def extract(): 
    final_df = pd.DataFrame()
    data_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Data"))

    for path in glob.glob(data_folder_path + "\*.csv"):
        if os.path.basename(path) != "final_data.csv":
            curr_df = pd.read_csv(path)
            row_bool = curr_df.apply(lambda x: filter_using_keywords(x["Blog Title"].lower()), axis=1)
            curr_df = curr_df[row_bool]
            final_df = pd.concat([final_df, curr_df], ignore_index=True)

    # dropping rows conatining duplicate blog links
    final_df.drop_duplicates(subset=["Blog Link"], inplace=True, ignore_index=True)

    # replacing NaN with empty string
    final_df.fillna("", inplace=True)

    # saving combined data as csv
    SaveDataAsCSV.df_to_csv_in_data(dataframe=final_df, caller_path=__file__)

if __name__ == "__main__":
	print("Processing...")
	extract()
	print("Finished.")
