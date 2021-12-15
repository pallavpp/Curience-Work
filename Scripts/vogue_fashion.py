from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import requests
import os

def extract():
	page_no = 1
	column_names = ["Blog Title", "Blog Date", "Author Name", "Blog Link", "Thumbnail Link"]
	df = pd.DataFrame(columns=column_names)

	while True:
		html_response = requests.get(f"https://www.vogue.in/fashion?page={page_no}")
		if html_response.status_code != 200: 
			break
		else:
			page_no += 1
			html_text = html_response.text
			soup = BeautifulSoup(html_text, "lxml")
			dom = etree.HTML(str(soup))
			cards = dom.xpath(".//*[@class='summary-item__content']/..")
			if not len(cards):
				continue

		for card in cards:
			thumbnail_link = ""
			xpath_list = card.xpath('.//img/@src')
			if len(xpath_list): thumbnail_link = str(xpath_list[0])
			
			blog_title = ""
			xpath_list = card.xpath('.//h2//text()')
			for segments in xpath_list:
				blog_title += str(segments)
			
			blog_link = ""
			xpath_list = card.xpath('.//h2/../@href')
			if len(xpath_list): blog_link = "https://www.vogue.in" + str(xpath_list[0])

			author_name = ""
			xpath_list = card.xpath('.//p//text()')
			for segments in xpath_list:
				author_name += str(segments) + " "
			author_name = author_name.replace("By", "").replace("by", "").replace("and", "").strip()

			blog_date = ""
			xpath_list = card.xpath('.//div[contains(@class, "publish-date")]/text()')
			if len(xpath_list): blog_date = str(xpath_list[0])

			df.loc[len(df.index)] = [blog_title, blog_date, author_name, blog_link, thumbnail_link]

	csv_filename = os.path.basename(__file__).split('.')[0] + ".csv"
	csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Data", csv_filename))
	df.to_csv(csv_path, index=False)

if __name__ == "__main__":
	print("Processing...")
	extract();
	print("Finished.")
