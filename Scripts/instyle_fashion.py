# importing modules
import os
import sys

from bs4 import element
modules_path  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
if modules_path not in sys.path:
    sys.path.insert(1, modules_path)
import SaveDataAsCSV

# importing utilities
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import pandas as pd
import time

def extract():

    column_names = ['Blog Title', 'Blog Link', 'Thumbnail Link']
    df = pd.DataFrame(columns=column_names)

    print('Opening the wbsite window in Chrome Browser');

    website = 'https://www.instyle.com/fashion/clothing'
    s=Service('E:\chromedriver\chromedriver.exe') # the path where the chrodriver.exe file is located locally
    driver = webdriver.Chrome(service=s)

    print('Maximizing the window');
    driver.maximize_window()
    driver.get(website)

    print('Waiting for 30 seconds for the first pop-up to load')
    time.sleep(30)

    try: # for closing the first pop-up
        notification_path = '//button[@class="pushly_popover-buttons-dismiss pushly-prompt-buttons-dismiss"]'
        notification = driver.find_element(By.XPATH, notification_path)
        notification.click()
        time.sleep(30)

        print('')
        print('First pop-up closed')
        print('')
    except:
        pass

    page_no = 1 
    card_no = 1 # for processing the cards in page number 1
    card_no1 = 1 # for processing the cards from page no 2 onwards

    print('Scraping work begins...')

    while page_no <= 20: # only scraping till page no 20 as blogs are from 2019 and earlier
        if page_no == 1:
            while True: # runs until no more card is left to be scraped on current page
                try: # for closing the haircut inspiration pop-up 
                    driver.find_element(By.XPATH, '//a[@id="bx-close-inside-1478537"]').click()
                    print('')
                    print('Haircut Inspiration pop-up closed')
                    print('')
                except:
                    pass
                try: # for closing the second pop-up 
                    driver.find_element(By.XPATH, '//div[@class="bx-row bx-row-submit bx-row-submit-no  bx-row-bK4PHgF bx-element-1497904-bK4PHgF"]/button').click()
                    print('')
                    print('Second pop-up closed')
                    print('')
                except:
                    pass
                try:
                    path = '//div[@class="category-page-item"]'
                    path += ('[' + str(card_no) + ']')
                    card = driver.find_element(By.XPATH, path)

                    blog_text = card.find_element(By.XPATH, './/span[@class="category-page-item-title linkHoverStyle"]').text

                    # image and text are inside two div tags of different classes hence we are making two different elements to scrap them

                    element1 = card.find_element(By.XPATH, './/img')
                    thumbnail_link = str(element1.get_attribute('src'))

                    if thumbnail_link.startswith('data'): # if we get a faulty thumbnail link
                        thumbnail_link = ""

                    element2 = card.find_element(By.XPATH, './/div[@class="category-page-item-content"]/a')
                    blog_link = str(element2.get_attribute('href'))

                    df.loc[len(df.index)] = [blog_text, blog_link, thumbnail_link] # adding the row containing desired values in the dataframe

                    # debugging stuffs
                    print(card_no, blog_text)
                    print(blog_link)
                    print(thumbnail_link)
                    print("")

                    card_no += 1
                except:
                    break

            try:
                button = driver.find_element(By.XPATH, '//a[@id="category-page-list-related-load-more-button"]')
                button.click()
                time.sleep(5)
            except:
                break

            page_no += 1

        else:
            while True:
                try:
                    driver.find_element(By.XPATH, '//a[@id="bx-close-inside-1478537"]').click()
                    print('')
                    print('Haircut Inspiration pop-up closed')
                    print('')
                except:
                    pass
                try:
                    driver.find_element(By.XPATH, '//div[@class="bx-row bx-row-submit bx-row-submit-no  bx-row-bK4PHgF bx-element-1497904-bK4PHgF"]/button').click()
                    print('')
                    print("Notification on the left side of the screen is closed")
                    print('')
                except:
                    pass
                try:
                    path = '//div[@class="category-page-item "]'  
                    path += ('[' + str(card_no1) + ']')
                    card = driver.find_element(By.XPATH, path)

                    blog_text = card.find_element(By.XPATH, './/span[@class="category-page-item-title linkHoverStyle"]').text

                    element1 = card.find_element(By.XPATH, './/img')
                    thumbnail_link = str(element1.get_attribute('src'))

                    if thumbnail_link.startswith('data'):
                        thumbnail_link = ""

                    element2 = card.find_element(By.XPATH, './/div[@class="category-page-item-content"]/a')
                    blog_link = str(element2.get_attribute('href'))

                    df.loc[len(df.index)] = [blog_text, blog_link, thumbnail_link]

                    print(card_no, blog_text)
                    print(blog_link)
                    print(thumbnail_link)
                    print("")

                    card_no1 += 1
                    card_no += 1
                except:
                    break

            try:
                button = driver.find_element(By.XPATH, '//a[@id="category-page-list-related-load-more-button"]')
                button.click()
                time.sleep(5)
            except:
                break

            page_no += 1

    print('Scarped a total of ', card_no - 1, ' cards')

    SaveDataAsCSV.df_to_csv_in_data(df, __file__)
    
    driver.quit()

if __name__ == "__main__":
    print('Processing...')
    extract()
    print('Finished')