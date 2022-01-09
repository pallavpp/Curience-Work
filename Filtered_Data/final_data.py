# standard imports
import pandas as pd

# custom imports
import os
import sys
modules_path  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
if modules_path not in sys.path:
    sys.path.insert(1, modules_path)
import SaveDataAsCSV
import re

def remove_redundant_blogs(final_df):
    pattern = re.compile(r'20\d\d') # using regex to find matches
    for index, row in final_df.iterrows():
        title = str(row["Blog Title"])
        matches = pattern.finditer(title) # returns all iterators

        matched_years = []
        for match in matches:
            matched_years.append(int(str(match.group(0))))
        
        # deleting rows containg years from 2010-2021
        if len(matched_years) > 0:
            if 2022 in matched_years:
                continue
            else:                
                for year in matched_years:
                    if year >= 2010 and year <= 2021:
                        final_df.at[index, "keyword_count"] = 0
                        break
        
        # working with Blog Date column
        blog_date = str(row["Blog Date"])
        date_matches = pattern.finditer(blog_date)

        dates = []
        for date in date_matches:
            dates.append(int(str(date.group(0))))

        # resetting values for sorting later
        if len(dates) > 0:
            if dates[0] < 2021:
                final_df.at[index, "keyword_count"] = 0

# main process
def extract(max_rows):
    # reading csv
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cumulative_data_with_keyword_count.csv"))
    final_df = pd.read_csv(path)

    remove_redundant_blogs(final_df)

    # dropping rows conatining duplicate blog links
    final_df.drop_duplicates(subset=["Blog Link"], inplace=True, ignore_index=True)

    # replacing NaN with empty string
    final_df.fillna("", inplace=True)

    # sort and save cumulative data
    final_df.sort_values(by="keyword_count", ascending=False, inplace=True)
    final_df.reset_index
    final_df.drop("keyword_count", axis=1, inplace=True)

    # saving combined data as csv
    if final_df.shape[0] > max_rows:
        final_df = final_df.iloc[:max_rows]
    SaveDataAsCSV.df_to_csv_in_currdir(dataframe=final_df, caller_path=__file__)

if __name__ == "__main__":
    print("Processing...")

    # maximum number of rows in output
    max_rows_in_output = 100
    
    extract(max_rows=max_rows_in_output)
    print("Finished.")