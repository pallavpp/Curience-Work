# standard imports
import pandas as pd
import re

# custom imports
import os

def calculate_recall():
    path_of_fashion_intern_data = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "Read_Files/fashion_intern_forecasting_website_list.csv"))
    path_of_cumulative_data = os.path.abspath(os.path.join(os.path.dirname(__file__), "final_data.csv"))

    fashion_intern_df = pd.read_csv(path_of_fashion_intern_data)
    cumulative_data_df = pd.read_csv(path_of_cumulative_data)

    matched_blog_links = []

    for index_cumulative_data, row_cumulative_data in cumulative_data_df.iterrows():
        cumulative_data_blog_link = str(row_cumulative_data["Blog Link"])
        
        for index_fashion_intern, row_fashion_intern in fashion_intern_df.iterrows():
            fashion_intern_blog_link = str(row_fashion_intern["Website URL"])

            if fashion_intern_blog_link == cumulative_data_blog_link and fashion_intern_blog_link not in matched_blog_links:
                matched_blog_links.append(fashion_intern_blog_link)
    
    print("Mached blogs are:")
    for blog_link in matched_blog_links:
        print(blog_link)
    print(len(matched_blog_links), "blogs are maching.") 

if __name__ == "__main__":
    print("Processing")
    calculate_recall()
    print("Finished")
