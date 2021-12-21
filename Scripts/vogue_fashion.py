# standard imports
from bs4 import BeautifulSoup
from lxml import etree
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
	column_names = ["Blog Title", "Blog Date", "Author Name", "Blog Link", "Thumbnail Link"]
	df = pd.DataFrame(columns=column_names)

	while True:
		# all blog cards as etree
		html_response = requests.get(f"https://www.vogue.in/fashion?page={page_no}")
		if html_response.status_code != 200: 
			break
		else:
			print(f"Getting page {page_no}")
			page_no += 1
			html_text = html_response.text
			soup = BeautifulSoup(html_text, "lxml")
			dom = etree.HTML(str(soup))
			cards = dom.xpath(".//*[@class='summary-item__content']/..")
			if not len(cards):
				continue

		# blog data
		for card in cards:
			# thumbnail link
			thumbnail_link = ""
			xpath_list = card.xpath('.//img/@src')
			if len(xpath_list): thumbnail_link = str(xpath_list[0])
			
			# blog title
			blog_title = ""
			xpath_list = card.xpath('.//h2//text()')
			for segments in xpath_list:
				blog_title += str(segments)
			
			# blog link
			blog_link = ""
			xpath_list = card.xpath('.//h2/../@href')
			if len(xpath_list): blog_link = "https://www.vogue.in" + str(xpath_list[0])

			# author name
			author_name = ""
			xpath_list = card.xpath('.//p//text()')
			for segments in xpath_list:
				author_name += str(segments) + " "
			author_name = author_name.replace("By", "").replace("by", "").replace("and", "").strip()

			# blog date
			blog_date = ""
			xpath_list = card.xpath('.//div[contains(@class, "publish-date")]/text()')
			if len(xpath_list): blog_date = str(xpath_list[0])

			# adding data to dataframe
			df.loc[len(df.index)] = [blog_title, blog_date, author_name, blog_link, thumbnail_link]

	# saving data as csv
	print("Saving data")
	SaveDataAsCSV.df_to_csv_in_data(dataframe=df, caller_path=__file__)

if __name__ == "__main__":
	print("Processing...")
	extract();
	print("Finished.")
