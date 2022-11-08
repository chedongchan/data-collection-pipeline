from tkinter import image_names
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import re
import os
from datetime import datetime
import json

url = "https://soundcloud.com/mangrymade"
driver = webdriver.Chrome() 
URL = url 
driver.get(URL)
delay=10
artists = []
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-button-group"]')))
    print("Frame Ready!")
    accept_cookies_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
    print("Accept Cookies Button Ready!")
    accept_cookies_button.click()
    time.sleep(1)

except TimeoutException:
    print("Loading took too much time!")

    time.sleep(2)

driver.current_url
related_artists_links = driver.find_elements(by=By.XPATH, value= './/h3[@class="userBadge__username sc-type-light sc-text-secondary sc-text-h4"]')
for i in range(3):
    driver.current_url
    if related_artists_links[0] in artists:
        artist_href_tag = related_artists_links[1].find_element(by=By.XPATH, value= './/a').get_attribute("href")
        print(artist_href_tag)
        driver.execute_script("window.scrollTo(0, 0);")
        artists.append(related_artists_links[1].find_element(by=By.XPATH, value= './/a').get_attribute("textContent"))
        related_artists_links[1].find_element(by=By.XPATH, value= './/a').click()

    elif related_artists_links[1] not in artists:
        artist_href_tag = related_artists_links[1].find_element(by=By.XPATH, value= './/a').get_attribute("href")
        print(artist_href_tag)
        driver.execute_script("window.scrollTo(0, 0);")
        artists.append(related_artists_links[1].find_element(by=By.XPATH, value= './/a').get_attribute("textContent"))
        related_artists_links[1].find_element(by=By.XPATH, value= './/a').click()
        
    else: 
        artist_href_tag = related_artists_links[2].find_element(by=By.XPATH, value= './/a').get_attribute("href")
        print(artist_href_tag)
        driver.execute_script("window.scrollTo(0, 0);")
        artists.append(related_artists_links[2].find_element(by=By.XPATH, value= './/a').get_attribute("textContent"))
        related_artists_links[2].find_element(by=By.XPATH, value= './/a').click()

    related_artists_links = driver.find_elements(by=By.XPATH, value= './/h3[@class="userBadge__username sc-type-light sc-text-secondary sc-text-h4"]')
    i+=1

print(artists)