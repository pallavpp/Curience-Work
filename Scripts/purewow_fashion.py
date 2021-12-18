from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

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
while True:
    try:
        more_button = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH, "//div[@class='container show-more-container']//a[@href='javascript:void(0);']")))
    except TimeoutException:
        flag = 1
        print("TimeoutException: All clicks successful")
        break
    except:
        print("Some error occured while clicking more_button")
        break
    else:
        more_button.click()

if flag:
    pass

driver.quit()
