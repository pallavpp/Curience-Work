# standard imports
from bs4 import BeautifulSoup
import pandas as pd
import requests

# custom imports
import os
import sys
modules_path  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
if modules_path not in sys.path:
    sys.path.insert(1, modules_path)
import SaveDataAsCSV

# main process
def extract():
	# variables
	page_no = 1
	column_names = ["Blog Title", "Blog Date", "Author Name", "Blog Link", "Author Profile Link", "Thumbnail Link"]
	df = pd.DataFrame(columns=column_names)

	while True:
		html_response = requests.get(f"https://thevou.com/fashion/page/{page_no}/")
		if html_response.status_code != 200: 
			break
		else:
			print(f"Getting page {page_no}")
			page_no += 1
		
		# all blog cards
		html_text = html_response.text
		soup = BeautifulSoup(html_text, "lxml")
		cards = soup.find_all("div", class_="td-module-container td-category-pos-above")

		# saving blog data
		for card in cards:
			image_link = card.find("div", class_="td-module-thumb").a.span["data-bg"]
			blog_link = card.find("div", class_="td-module-thumb").a["href"]
			blog_title = card.find("h3", class_="entry-title td-module-title").a.text.strip()
			author_page = card.find("span", class_="td-post-author-name").a["href"]
			author_name = card.find("span", class_="td-post-author-name").a.text.strip()
			blog_text = requests.get(blog_link).text
			blog_soup = BeautifulSoup(blog_text, "lxml")
			blog_date = blog_soup.find("time", class_="entry-date updated td-module-date").text
			df.loc[len(df.index)] = [blog_title, blog_date, author_name, blog_link, author_page, image_link]

	# saving data as csv
	print("Saving data")
	SaveDataAsCSV.df_to_csv_in_data(dataframe=df, caller_path=__file__)

if __name__ == "__main__":
	print("Processing...")
	extract()
	print("Finished.")
