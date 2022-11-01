from scrapper import Scrapper
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


if __name__ == "__main__":
    zoopla = Scrapper()
    driver = zoopla.load_and_accept_cookies()
    tags= zoopla.get_tags(driver)
    links= zoopla.create_links(tags)
    multi_links = zoopla.multi_page_links(driver)
    dict_properties, key1, key2, key3, key4 = zoopla.data_format()
    data= zoopla.collect_data(multi_links,dict_properties,key1,key2,key3,key4,driver)
    zoopla.print_data(data)


