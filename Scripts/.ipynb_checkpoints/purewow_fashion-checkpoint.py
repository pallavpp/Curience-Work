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

# time.sleep(10)

flag = 0
var = 2
temp = 0
while True:
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
        temp += 1
        print("No TimeoutException: Single click successful")
        if temp == var:
            flag = 1
            print("No TimeoutException: All clicks successful")
            break

# time.sleep(10)

blog_titles = []
blog_dates = []
author_names = []
blog_links = []
author_profile_links = []
thumbnail_links = []
thumbnail_credits = []

if flag:
    print("Inside if")

    try:
        WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, "//div[@class='row slide-content']")))
    except TimeoutException:
        print("TimeoutException: No cards_sliding found")
    except:
        print("Some error while waiting for cards_sliding")
    else:
        cards_sliding = driver.find_elements_by_xpath("//div[@class='row slide-content']")
        print(len(cards_sliding))

    try:
        WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, "//div[@class='col-sm-6 ']")))
    except TimeoutException:
        print("TimeoutException: No cards_big found")
    except:
        print("Some error while waiting for cards_big")
    else:
        cards_big = driver.find_elements_by_xpath("//div[@class='col-sm-6 ']")
        print(len(cards_big))
    
    try:
        WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, "//div[@class='col-sm-4' or @class='col-sm-4 ']")))
    except TimeoutException:
        print("TimeoutException: No cards_normal found")
    except:
        print("Some error while waiting for cards_normal")
    else:
        cards_normal = driver.find_elements_by_xpath("//div[@class='col-sm-4' or @class='col-sm-4 ']")
        print(len(cards_normal))

    for card in cards_sliding:
        blog_title = ""
        element = driver.find_element_by_xpath(".//h1")
        if element: blog_title = element.text.strip()
        blog_titles.append(blog_title)

        thumbnail_credit = ""
        element = driver.find_element_by_xpath(".//span[@class='photo_credit']")
        if element: thumbnail_credit = element.text.strip()
        thumbnail_credits.append(thumbnail_credit)

        blog_link = ""
        element = driver.find_element_by_xpath(".//a")
        if element:
            element_href = str(element.get_attribute("href")).strip()
            if element_href[0] == '/':
                blog_link = "https://www.purewow.com" + element_href
            else:
                blog_link = element_href
        blog_links.append(blog_link)

        thumbnail_link = ""
        element = driver.find_element_by_xpath(".//img")
        if element: thumbnail_link = str(element.get_attribute("src")).strip()
        thumbnail_links.append(thumbnail_link)

        blog_dates.append("")
        author_names.append("")
        author_profile_links.append("")

    for card in cards_big:
        blog_title = ""
        element = driver.find_element_by_xpath(".//h4")
        if element: blog_title = element.text.strip()
        blog_titles.append(blog_title)

        thumbnail_credit = ""
        element = driver.find_element_by_xpath(".//span[@class='photo_credit']")
        if element: thumbnail_credit = element.text.strip()
        thumbnail_credits.append(thumbnail_credit)

        blog_link = ""
        element = driver.find_element_by_xpath(".//a")
        if element:
            element_href = str(element.get_attribute("href")).strip()
            if element_href[0] == '/':
                blog_link = "https://www.purewow.com" + element_href
            else:
                blog_link = element_href
        blog_links.append(blog_link)

        thumbnail_link = ""
        element = driver.find_element_by_xpath(".//img")
        if element: thumbnail_link = str(element.get_attribute("src")).strip()
        thumbnail_links.append(thumbnail_link)

        blog_dates.append("")
        author_names.append("")
        author_profile_links.append("")

    for card in cards_normal:
        blog_title = ""
        element = driver.find_element_by_xpath(".//h4")
        if element: blog_title = element.text.strip()
        blog_titles.append(blog_title)

        thumbnail_credit = ""
        element = driver.find_element_by_xpath(".//span[@class='photo_credit']")
        if element: thumbnail_credit = element.text.strip()
        thumbnail_credits.append(thumbnail_credit)

        blog_link = ""
        element = driver.find_element_by_xpath(".//a")
        if element:
            element_href = str(element.get_attribute("href")).strip()
            if element_href[0] == '/':
                blog_link = "https://www.purewow.com" + element_href
            else:
                blog_link = element_href
        blog_links.append(blog_link)

        thumbnail_link = ""
        element = driver.find_element_by_xpath(".//img")
        if element: thumbnail_link = str(element.get_attribute("src")).strip()
        thumbnail_links.append(thumbnail_link)

        blog_dates.append("")
        author_names.append("")
        author_profile_links.append("")

df = pd.DataFrame({"Blog Title": blog_titles, "Blog Date": blog_dates, "Author Name": author_names, "Thumbnail Credit": thumbnail_credits, "Blog Link": blog_links, "Author Profile Link": author_profile_links, "Thumbnail Link": thumbnail_links})
csv_filename = os.path.basename(__file__).split('.')[0] + ".csv"
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Data", csv_filename))
df.to_csv(csv_path, index=False)
print("df saved")

# driver.quit()
