# standard imports
import pandas as pd
import re

# custom imports
import os
import sys
modules_path  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
if modules_path not in sys.path:
    sys.path.insert(1, modules_path)
import SaveDataAsCSV

# function to return regex year matches
def find_year_matches(regex_pattern, str_to_find_from):
    matches = regex_pattern.finditer(str_to_find_from)
    match_list = []
    for match in matches:
        match_list.append(int(str(match.group(0))))
    return match_list

# function to remove old blogs with high keyword count
def improve_ranking(df):
    """
    If year present in Blog Date - remove if >= 2010 and <= 2021, keep if 2022 present.\n
    Keyword presence in title increases score by 1.\n
    If Blog Date or Blog/Thumbnail Link non empty and contain year < 2021 - remove if permitted.\n
    2022 in Blog Date/Link increases score by 1.
    \n
    Parameters:\n
    Pandas DataFrame
    """

    # regex pattern to find year
    pattern = re.compile(r'20\d\d')

    # resetting score for required rows
    for index, row in df.iterrows():
        # flags
        keyword_in_title_flag = False
        year_flag = False
        year_in_title_flag = False

        # removing rows containg years from 2010-2021 in title
        title = str(row["Blog Title"])
        years_matched = find_year_matches(regex_pattern=pattern, str_to_find_from=title)

        for year in years_matched:
            if year >= 2010 and year <= 2021:
                df.at[index, "Score"] = 0
                break
        if df.at[index, "Score"] == 0:
            continue

        # bonus score for useful keywords in blog title
        if "summer" in title.lower():
            keyword_in_title_flag = True
        if "spring" in title.lower():
            keyword_in_title_flag = True
        if 2022 in years_matched:
            keyword_in_title_flag = True
            year_in_title_flag = True
        
        # removing blogs older than 2021 or with blog/thumbnail link containing years less than 2021
        blog_date = str(row["Blog Date"])
        blog_link = str(row["Blog Link"])
        thumbnail_link = str(row["Thumbnail Link"])
        blog_date_years_matched = find_year_matches(regex_pattern=pattern, str_to_find_from=blog_date)
        blog_link_years_matched = find_year_matches(regex_pattern=pattern, str_to_find_from=blog_link)
        thumbnail_link_years_matched = find_year_matches(regex_pattern=pattern, str_to_find_from=thumbnail_link)

        for year in (blog_date_years_matched + blog_link_years_matched + thumbnail_link_years_matched):
            if year_in_title_flag == False and year < 2021:
                df.at[index, "Score"] = 0
                break
        if df.at[index, "Score"] == 0:
            continue

        # bonus score for year in blog link
        if 2022 in (blog_date_years_matched + blog_link_years_matched):
            year_flag = True

        # bonus scores
        if keyword_in_title_flag:
            df.at[index, "Score"] = df.at[index, "Score"] + 1
        if year_flag:
            df.at[index, "Score"] = df.at[index, "Score"] + 1

# main process
def extract(max_rows):
    # reading csv with cumulative data
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cumulative_data_with_keyword_count.csv"))
    final_df = pd.read_csv(path)
    final_df.rename(columns={"keyword_count": "Score"}, inplace=True)

    # removing false blogs with high score
    improve_ranking(df=final_df)

    # fixing data
    final_df.drop_duplicates(subset=["Blog Link"], inplace=True, ignore_index=True)
    final_df.fillna("", inplace=True)

    # sort data and find max useful result
    final_df.sort_values(by="Score", ascending=False, inplace=True)
    final_df.reset_index
    last_useful_data = 0
    for value in final_df["Score"]:
        if value > 0:
            last_useful_data += 1
        else:
            break
    final_df.drop("Score", axis=1, inplace=True)

    # saving data as csv
    final_df = final_df.iloc[:min(max_rows, last_useful_data)]
    SaveDataAsCSV.df_to_csv_in_currdir(dataframe=final_df, caller_path=__file__)

if __name__ == "__main__":
    print("Processing...")

    # maximum number of rows in output
    max_rows_in_output = 100
    
    extract(max_rows=max_rows_in_output)
    print("Finished.")
