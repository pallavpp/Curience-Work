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
    popup_iframe = WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, "//iframe[contains(@id, 'lightbox-iframe')]")))
except TimeoutException:
    print("TimeoutException: Popup was not visible in 30s")
    driver.quit()
else:
    driver.switch_to.frame(popup_iframe)
    skip_popup_button = driver.find_element_by_xpath("//*[@id='layout']//button[text()='NO THANKS']")
    skip_popup_button.click()
    driver.switch_to.default_content()

# while True:
#     count = 0
#     try:
#         button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "More")))
#     except TimeoutException:
#         break






# while True:
#     time.sleep(1)
#     driver.find_element_by_link_text("More").click()







# all_matches_button = driver.find_element_by_xpath("//label[@analytics-event='All matches']")
# all_matches_button.click()

# dropdown = Select(driver.find_element_by_id("country"))
# dropdown.select_by_visible_text("Spain")
# time.sleep(3)

# matches = driver.find_elements_by_tag_name("tr")
# date = []
# home_team = []
# score = []
# away_team = []

# for match in matches:
#     date.append(match.find_element_by_xpath("./td[1]").text)
#     home = match.find_element_by_xpath("./td[2]").text
#     home_team.append(home)
#     print(home)
#     score.append(match.find_element_by_xpath("./td[3]").text)
#     away_team.append(match.find_element_by_xpath("./td[4]").text)









# print(count)

# driver.quit()
