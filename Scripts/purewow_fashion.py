from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import requests
import os

path = "D:\Selenium\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.maximize_window()
website = 'https://www.purewow.com/fashion'
driver.get(website)

try:
    popup_iframe = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH, "//iframe[contains(@id, 'lightbox-iframe')]")))
except TimeoutException:
    print("TimeoutException: Popup was not visible in 60s, assume no popup")
except:
    print("Some error occured while waiting for popup")
else:
    driver.switch_to.frame(popup_iframe)
    skip_popup_button = driver.find_element_by_xpath("//*[@id='layout']//button[text()='NO THANKS']")
    skip_popup_button.click()
    driver.switch_to.default_content()
    print("Popup closed successfully")

flag = 0
# while True:
try:
    more_button = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH, "//div[@class='container show-more-container']//a[@href='javascript:void(0);']")))
except TimeoutException:
    # flag = 1
    print("TimeoutException: All clicks successful")
    # break
except:
    print("Some error occured while clicking more_button")
    # break
else:
    more_button.click()
    flag = 1
    print("No TimeoutException: Single click successful")

blog_titles = []
blog_dates = []
author_names = []
blog_links = []
author_profile_links = []
thumbnail_links = []
thumbnail_credits = []

if flag:
    cards_sliding = driver.find_elements_by_xpath("//div[@class='row slide-content']")
    cards_big = driver.find_elements_by_xpath("//div[@class='col-sm-6']//span[@class='photo_credit']/ancestor::div[@class='col-sm-6']")
    cards_normal = driver.find_elements_by_xpath("//div[@class='col-sm-4']")

    for card in cards_sliding:
        blog_title = ""
        blog_title_segments = driver.find_elements_by_xpath(".//h1//text()")
        for segment in blog_title_segments:
            blog_title += str(segment)
        blog_titles.append(blog_title)

        thumbnail_credit = ""
        element = driver.find_element_by_xpath(".//span[@class='photo_credit']/text()")
        if element: thumbnail_credit = str(element)
        thumbnail_credits.append(thumbnail_credit)

        blog_link = ""
        element = driver.find_element_by_xpath(".//a/@href")
        if element:
            if element[0] == '/':
                blog_link = "https://www.purewow.com" + blog_link
            else:
                blog_link = str(element)
        blog_links.append(blog_link)

        thumbnail_link = ""
        element = driver.find_element_by_xpath(".//img/@src")
        if element: thumbnail_link = str(element)
        thumbnail_links.append(thumbnail_link)

        blog_dates.append("")
        author_names.append("")
        author_profile_links.append("")

    for card in cards_big:
        blog_title = ""
        blog_title_segments = driver.find_elements_by_xpath(".//h4//text()")
        for segment in blog_title_segments:
            blog_title += str(segment)
        blog_titles.append(blog_title)

        thumbnail_credit = ""
        element = driver.find_element_by_xpath(".//span[@class='photo_credit']/text()")
        if element: thumbnail_credit = str(element)
        thumbnail_credits.append(thumbnail_credit)

        blog_link = ""
        element = driver.find_element_by_xpath(".//a/@href")
        if element:
            if element[0] == '/':
                blog_link = "https://www.purewow.com" + blog_link
            else:
                blog_link = str(element)
        blog_links.append(blog_link)

        thumbnail_link = ""
        element = driver.find_element_by_xpath(".//img/@src")
        if element: thumbnail_link = str(element)
        thumbnail_links.append(thumbnail_link)

        blog_dates.append("")
        author_names.append("")
        author_profile_links.append("")

    for card in cards_normal:
        blog_title = ""
        blog_title_segments = driver.find_elements_by_xpath(".//h4//text()")
        for segment in blog_title_segments:
            blog_title += str(segment)
        blog_titles.append(blog_title)

        thumbnail_credit = ""
        element = driver.find_element_by_xpath(".//span[@class='photo_credit']/text()")
        if element: thumbnail_credit = str(element)
        thumbnail_credits.append(thumbnail_credit)

        blog_link = ""
        element = driver.find_element_by_xpath(".//a/@href")
        if element:
            if element[0] == '/':
                blog_link = "https://www.purewow.com" + blog_link
            else:
                blog_link = str(element)
        blog_links.append(blog_link)

        thumbnail_link = ""
        element = driver.find_element_by_xpath(".//img/@src")
        if element: thumbnail_link = str(element)
        thumbnail_links.append(thumbnail_link)

        blog_dates.append("")
        author_names.append("")
        author_profile_links.append("")

df = pd.DataFrame({"Blog Title": blog_titles, "Blog Date": blog_dates, "Author Name": author_names, "Thumbnail Credit": thumbnail_credits, "Blog Link": blog_links, "Author Profile Link": author_profile_links, "Thumbnail Link": thumbnail_links})
csv_filename = os.path.basename(__file__).split('.')[0] + ".csv"
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Data", csv_filename))
df.to_csv(csv_path, index=False)

driver.quit()
