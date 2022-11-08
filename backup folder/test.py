from selenium import webdriver 
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.find_element(by=By.XPATH, value='//button')
my_path = driver.find_element(by=By.XPATH, value='//*[@id="__next"]')
new_path = my_path.find_element(by=By.XPATH, value='./div')