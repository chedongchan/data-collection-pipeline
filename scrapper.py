from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


#run python test_scrapper.py to test the code.


class Scrapper:
    def __init__(self) -> None:
        self.url = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
        
    
    def load_and_accept_cookies(self)-> webdriver.Chrome:
        '''
        Open Zoopla and accept the cookies
        
        Returns
        -------
        driver: webdriver.Chrome
            This driver is already in the Zoopla webpage
        '''
        driver = webdriver.Chrome() 
        URL = self.url 
        driver.get(URL)
        delay = 10 
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gdpr-consent-notice"]')))
            print("Frame Ready!")
            driver.switch_to.frame('gdpr-consent-notice')
            accept_cookies_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="save"]')))
            print("Accept Cookies Button Ready!")
            accept_cookies_button.click()
            time.sleep(1)

        except TimeoutException:
            print("Loading took too much time!")

        return driver 

    def get_tags(self,driver):
        '''
        Returns a list with all the links in the current page
        Parameters
        ----------
        driver: webdriver.Chrome
            The driver that contains information about the current page
        
        Returns
        -------
        link_list: list
            A list with all the links in the page
        '''
        prop_container = driver.find_element(by=By.XPATH, value='//div[@data-testid="regular-listings"]')# change to fit the id of the html tag
        prop_list = prop_container.find_elements(by=By.XPATH, value='./div')

        return prop_list

    def create_links(self,prop_list):

        link_list = []

        for house_property in prop_list:
            a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            link_list.append(link)

        return link_list
    
    def multi_page_links(self,driver):
        big_list = []
        num_pages = input('How many pages do you want to collect data from?')
        for i in range(int(num_pages)): # The first 5 pages only
            big_list.extend(self.create_links(self.get_tags(driver))) 
            pagination = driver.find_element(by=By.XPATH, value='//a[@class="eaoxhri5 css-xtzp5a-ButtonLink-Button-StyledPaginationLink eaqu47p1"]') #change to match the next page class
            pagination.click()
            time.sleep(1)  
        
        return big_list

    def data_format(self):
        key1 = input("What data type do you want? 1")
        key2 = input("What data type do you want? 2")
        key3 = input("What data type do you want? 3")
        key4 = input("What data type do you want? 4")
        dict_properties = {str(key1): [], str(key2): [], str(key3): [], str(key4): []}

        return dict_properties, key1, key2, key3, key4

    def collect_data(self, big_list, dict_properties, key1, key2, key3, key4, driver):
        for link in big_list:
            
            driver.get(link)
            time.sleep(3)
            value1 = driver.find_element(by=By.XPATH, value='//p[@data-testid="price"]').text
            dict_properties[key1].append(value1)
            value2 = driver.find_element(by=By.XPATH, value='//address[@data-testid="address-label"]').text
            dict_properties[key2].append(value2)
            value3 = driver.find_element(by=By.XPATH, value='//div[@class="c-PJLV c-PJLV-iiNveLf-css"]').text
            dict_properties[key3].append(value3)
            div_tag = driver.find_element(by=By.XPATH, value='//div[@data-testid="truncated_text_container"]')
            span_tag = div_tag.find_element(by=By.XPATH, value='.//span')
            value4 = span_tag.text
            dict_properties[key4] = value4

        return dict_properties

    def search(self):
        pass

    def print_data(self, dict_properties):
        print(dict_properties)

    def scroll_page(self):
        pass
    
    def login(self):
        pass

