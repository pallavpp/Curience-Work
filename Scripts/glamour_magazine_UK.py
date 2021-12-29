import os
import sys
modules_path  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
if modules_path not in sys.path:
    sys.path.insert(1, modules_path)
import SaveDataAsCSV

from bs4 import BeautifulSoup
from lxml import etree
import requests
import pandas as pd

def scrap():
    page_no = 1
    column_names = ['Blog Category', 'Blog Title', 'Blog Catchphrase', 'Blog Link', 'Author Name', 'Thumbnail Link']
    df = pd.DataFrame(columns=column_names)

    while True:
        html_response = requests.get(f'https://www.glamourmagazine.co.uk/topic/fashion?page={page_no}')
        if html_response.status_code != 200:
            break
        else:
            html_text = html_response.text
            soup = BeautifulSoup(html_text, 'lxml')
            dom = etree.HTML(str(soup))
            cards1 = dom.xpath('.//*[@class="summary-item summary-item--has-border summary-item--has-rule summary-item--article summary-item--no-icon summary-item--text-align-left summary-item--layout-placement-side-by-side-desktop-only summary-item--layout-position-image-left summary-item--layout-proportions-50-50 summary-item--side-by-side-align-center summary-item--standard SummaryItemWrapper-gdEuvf cyHkuS summary-list__item"]')
            cards2 = dom.xpath('.//*[@class="summary-item summary-item--has-border summary-item--has-rule summary-item--gallery summary-item--no-icon summary-item--text-align-left summary-item--layout-placement-side-by-side-desktop-only summary-item--layout-position-image-left summary-item--layout-proportions-50-50 summary-item--side-by-side-align-center summary-item--standard SummaryItemWrapper-gdEuvf cyHkuS summary-list__item"]')
            if len(cards1):
                for card in cards1:
                    blog_category = ""
                    xpath_list = card.xpath('.//span[@class="RubricName-eZaHyj FsKDn"]//text()')
                    if len(xpath_list):
                        blog_category = str(xpath_list[0])

                    blog_title = ""
                    xpath_list = card.xpath('.//h3//text()')
                    for segments in xpath_list:
                        blog_title += str(segments)

                    blog_snippet = ""
                    xpath_list = card.xpath('.//p[@class="summary-item__dek"]//text()')
                    for segments in xpath_list:
                        blog_snippet += str(segments)

                    blog_link = ""
                    xpath_list = card.xpath('.//div[@class="summary-item__content"]/a/@href')
                    if len(xpath_list):
                        blog_link = "https://www.glamourmagazine.co.uk" + str(xpath_list[0])

                    blog_writer = ""
                    xpath_list = card.xpath('.//span[@class="BylineName-cKXFOb irUMly byline__name"]//text()')
                    for segments in xpath_list:
                        blog_writer += str(segments) + " "

                    img_src = ""
                    xpath_list = card.xpath('.//img/@src')
                    if len(xpath_list):
                        img_src = str(xpath_list[0])

                    df.loc[len(df.index)] = [blog_category, blog_title, blog_snippet, blog_link, blog_writer, img_src]

            if len(cards2):
                for card in cards2:
                    blog_category = ""
                    xpath_list = card.xpath('.//span[@class="RubricName-eZaHyj FsKDn"]//text()')
                    if len(xpath_list):
                        blog_category = str(xpath_list[0])

                    blog_title = ""
                    xpath_list = card.xpath('.//h3//text()')
                    for segments in xpath_list:
                        blog_title += str(segments)

                    blog_snippet = ""
                    xpath_list = card.xpath('.//p[@class="summary-item__dek"]//text()')
                    for segments in xpath_list:
                        blog_snippet += str(segments)

                    blog_link = ""
                    xpath_list = card.xpath('.//div[@class="summary-item__content"]/a/@href')
                    if len(xpath_list):
                        blog_link = "https://www.glamourmagazine.co.uk" + str(xpath_list[0])

                    blog_writer = ""
                    xpath_list = card.xpath('.//span[@class="BylineName-cKXFOb irUMly byline__name"]//text()')
                    for segments in xpath_list:
                        blog_writer += str(segments) + " "

                    img_src = ""
                    xpath_list = card.xpath('.//img/@src')
                    if len(xpath_list):
                        img_src = str(xpath_list[0])

                    df.loc[len(df.index)] = [blog_category, blog_title, blog_snippet, blog_link, blog_writer, img_src]

            print(f'page {page_no} done')
            page_no += 1
            
    SaveDataAsCSV.df_to_csv_in_data(df, __file__)


if __name__ == "__main__":
    print("Processing...")
    scrap()
    print("Finished.")