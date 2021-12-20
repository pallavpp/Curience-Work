# standard imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from dataclasses import dataclass
import time

# custom imports
import os
import sys
modules_path  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
if modules_path not in sys.path:
    sys.path.insert(1, modules_path)
import SaveDataAsCSV

# dataclass defined to store all scraped data
@dataclass
class blog_data:
    blog_title: str
    blog_date: str
    author_name: str
    blog_link: str
    author_profile_link: str
    thumbnail_link: str
    thumbnail_credit: str

all_data = []
column_names = ["Blog Title", "Blog Date", "Author Name", "Blog Link", "Author Profile Link", "Thumbnail Link", "Thumbnail Credit"]

# function to extract data from cards
def extract_data_from_cards(*card_types):
    """
    Traverses and extracts data from all cards passed.\n
    \n
    Parameters:\n
    Takes variable number of lists, each list is of a specific card type
    """
    
    for card_type in card_types:
        for card in card_type:
            # blog title
            try:
                element = card.find_element_by_xpath(".//h1")
            except NoSuchElementException:
                try:
                    element = card.find_element_by_xpath(".//h4")
                except NoSuchElementException:
                    card_blog_title = ""
                else:
                    card_blog_title = element.text.strip()
            else:
                card_blog_title = element.text.strip()

            # blog link
            try:
                element = card.find_element_by_xpath(".//a")
            except NoSuchElementException:
                card_blog_link = ""
            else:
                element_href = str(element.get_attribute("href")).strip()
                if element_href[0] == '/':
                    card_blog_link = "https://www.purewow.com" + element_href
                else:
                    card_blog_link = element_href

            # thumbnail link
            try:
                element = card.find_element_by_xpath(".//img")
            except NoSuchElementException:
                card_thumbnail_link = ""
            else:
                card_thumbnail_link = str(element.get_attribute("src")).strip()

            # thumbnail credit
            try:
                element = card.find_element_by_xpath(".//span[@class='photo_credit']")
            except NoSuchElementException:
                card_thumbnail_credit = ""
            else:
                card_thumbnail_credit = element.text.strip()

            # add data to list
            all_data.append(blog_data(card_blog_title, "", "", card_blog_link, "", card_thumbnail_link, card_thumbnail_credit))

# main process
def extract():
    # driver
    print("Opening driver")
    driver_path = "D:\Selenium\chromedriver.exe"
    driver = webdriver.Chrome(driver_path)
    driver.maximize_window()
    website = 'https://www.purewow.com/fashion'
    driver.get(website)

    # dealing with popup
    print("Dealing with popup")
    try:
        WebDriverWait(driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@id, 'lightbox-iframe')]")))
    except TimeoutException:
        print("TimeoutException: Popup not available in 60s, assume no popup")
    else:
        skip_popup_button = driver.find_element_by_xpath(".//*[@id='layout']//button[text()='NO THANKS']")
        skip_popup_button.click()
        driver.switch_to.default_content()

    # button clicks
    print("Performing button clicks")
    flag = 0
    click_count = 0
    while True:
        try:
            more_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='container show-more-container']//a[@href='javascript:void(0);']")))
        except TimeoutException:
            flag = 1
            print("TimeoutException: Assume all clicks are successful")
            break
        else:
            more_button.click()
            click_count += 1
            print(f"Click count: {click_count}")
            time.sleep(1)

    # there are three different types of blog cards on webpage which are stored in cards_sliding, cards_big and cards_normal
    if flag:
        print("Locating blog cards")
        # cards_sliding
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='row slide-content']")))
        except TimeoutException:
            print("TimeoutException: No cards_sliding found")
        else:
            cards_sliding = driver.find_elements_by_xpath("//div[@class='row slide-content']")

        # cards_big
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='col-sm-6 ']")))
        except TimeoutException:
            print("TimeoutException: No cards_big found")
        else:
            cards_big = driver.find_elements_by_xpath("//div[@class='col-sm-6 ']")
        
        # cards_normal
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='col-sm-4' or @class='col-sm-4 ']")))
        except TimeoutException:
            print("TimeoutException: No cards_normal found")
        else:
            cards_normal = driver.find_elements_by_xpath("//div[@class='col-sm-4' or @class='col-sm-4 ']")

        # extract data from cards
        print("Extracting data from cards")
        extract_data_from_cards(cards_sliding, cards_big, cards_normal)

    # saving data as csv
    SaveDataAsCSV.dataclass_to_csv_in_data(dataclass_list=all_data, column_name_list=column_names, caller_path=__file__)
    print("Saving data")
    driver.quit()

if __name__ == "__main__":
	print("Processing...")
	extract()
	print("Finished.")
