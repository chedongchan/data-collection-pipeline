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
import requests
from PIL import Image

#run python test_scrapper.py to test the code. Default link set to Zoopla website. Can chnage the URL to other websites..

class Scrapper:
    def __init__(self) -> None:
        self.url = "https://www.soundcloud.com"

    def load_and_accept_cookies(self)-> webdriver.Chrome:
        '''
        Open SoundCloud and accept the cookies
        
        Returns
        -------
        driver: webdriver.Chrome
            This driver is already in the SoundCloud webpage
        '''
        driver = webdriver.Chrome() 
        URL = self.url 
        driver.get(URL)
        delay = 10 
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

    def collect_data(self,driver):
            driver.current_url
            scroll_pause_time = 1
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                 # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(scroll_pause_time)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # try:
            #     WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="paging-eof sc-border-light-top"]')))
            #     print("Frame Ready!")
            #     accept_cookies_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            #     print("Accept Cookies Button Ready!")
            #     accept_cookies_button.click()
            #     time.sleep(1)

            # except TimeoutException:
            #     print("Loading took too much time!")

            # list of elements by unique ID.
            tracks_list = driver.find_elements(by=By.XPATH, value='//*[@class="sc-link-primary soundTitle__title sc-link-dark sc-text-h4"]')
            cover_art_list= driver.find_elements(by=By.XPATH, value='//a[@class="sound__coverArt"]')
            song_tags_list= driver.find_elements(by=By.XPATH, value='//a[@class="sc-tag soundTitle__tag sc-tag-small"]')
            ministats_list = driver.find_elements(by=By.XPATH, value='//span[@class="sc-ministats sc-ministats-small  sc-ministats-plays sc-text-secondary"]')

            # find title of song and add to list.
            songs=[]
            for track_atags in tracks_list[:-3]:
                song_title =track_atags.find_element(by=By.XPATH, value='.//span').get_attribute("textContent")

                songs.append(song_title)

            # find image links for each song.
            images =[]
            for cover_art in cover_art_list:
                span_tag = cover_art.find_element(by=By.XPATH, value='.//span')
                tag_attribute =span_tag.get_attribute('style')
                span_tag.location_once_scrolled_into_view
                time.sleep(1)
                cover_art_url =re.search('"(.*?)"',tag_attribute)
                images.append(cover_art_url.group(0))
            
            # find song genre tags.
            genre_tags = []
            for song_tag in song_tags_list:
                genre_tag = song_tag.find_element(by=By.XPATH, value='.//span[@class="sc-truncate sc-tagContent"]').get_attribute("textContent")
                genre_tags.append(genre_tag)
            
            # get number of times played for each song. 
            total_num_plays = []
            for stat in ministats_list[:-3]:
                num_plays = stat.find_element(by=By.XPATH, value='.//span[@aria-hidden="true"]').get_attribute("textContent")
                total_num_plays.append(num_plays)
            
            return songs, genre_tags, total_num_plays, images

    def get_timestamp(self):
        timestamp_now = datetime.now()
        str_date_time = timestamp_now.strftime("%d%m%Y_%H%M%S_")

        
        return str_date_time
    
    def search(self,driver):
        search_bar= driver.find_elements(by=By.XPATH, value='//*[@class="headerSearch__input sc-input g-all-transitions-300"]')
        search_bar[1].click()
        search_word = input("Which artist would you like info from?")
        search_bar[1].send_keys(search_word)
        time.sleep(1)
        search_bar[1].send_keys(Keys.RETURN)
        time.sleep(2)

        return search_word

    def filter_artist_results(self, driver):
        driver.current_url
        sidebar_elements = driver.find_element(by= By.XPATH, value='//*[@class="searchOptions__container"]')
        sidebar = sidebar_elements.find_elements(by= By.XPATH, value= './/li')
        people_option = sidebar[3]
        people_option.click()
        time.sleep(2)
    
    def artist_home_page(self,driver):
        driver.current_url
        artist_tags = driver.find_element(by= By.XPATH, value='//*[@class="sc-media-content"]')
        artist_link = artist_tags.find_element(by= By.XPATH, value= './/h2')
        artist_link_atag = artist_link.find_element(by= By.XPATH, value= './/a')
        artist_link_atag.click()
        time.sleep(2)
    
    def go_to_tracks_page(self,driver):
        driver.current_url
        track_tag = driver.find_elements(by= By.XPATH, value='//*[@class="g-tabs-link"]')
        track_tag[1].click()
        
        time.sleep(5)


    def generate_database(self, artist, songs, genre_tags, total_num_plays,images,timestamp):
        artist_database= {
        "Songs": songs,
        "Genre":genre_tags,
        "Play number": total_num_plays,
        "Image Link":images,
        }
        full_database = {"Name of Artist": artist,
        "Details":artist_database,
        "Timestamp":timestamp,
        }

        return full_database

    def make_data_folder(self,artist):
        current_dir = os.getcwd()
        raw_data_dir = current_dir +"\\raw_data"

        if not os.path.exists(raw_data_dir):
            os.makedirs(raw_data_dir)

        artist_dir =raw_data_dir + "\\" + artist

        if not os.path.exists(artist_dir):
            os.makedirs(artist_dir)

        image_save_dir=artist_dir +"\\" + 'images'

        if not os.path.exists(image_save_dir):
            os.makedirs(image_save_dir)

        return artist_dir, image_save_dir
    
    def save_dict_data_as_json(self,artist,full_database,artist_dir):
        with open(f'{artist_dir}\\{artist} soundcloud info.json','w') as fp:
            json.dump(full_database,fp,indent=4)
        database_dir =f'{artist_dir}\\{artist} soundcloud info.json'
        return database_dir

    def add_to_artist_list(self, search_word, artists):
        artists.append(search_word)
        return artists

    def related_artists(self, driver, artists):
        driver.current_url
        
        related_artists_links = driver.find_elements(by=By.XPATH, value= './/h3[@class="userBadge__username sc-type-light sc-text-secondary sc-text-h4"]')

        if related_artists_links[0] in artists:
            related_artists_links[1].find_element(by=By.XPATH, value= './/a').get_attribute("href")
            driver.execute_script("window.scrollTo(0, 0);")
            artists.append(related_artists_links[1].find_element(by=By.XPATH, value= './/span').get_attribute("textContent"))
            related_artists_links[1].find_element(by=By.XPATH, value= './/a').click()
        
        elif related_artists_links[1] not in artists:
            related_artists_links[1].find_element(by=By.XPATH, value= './/a')
            driver.execute_script("window.scrollTo(0, 0);")
            artists.append(related_artists_links[1].find_element(by=By.XPATH, value= './/span').get_attribute("textContent"))
            related_artists_links[1].find_element(by=By.XPATH, value= './/a').click()
            
        else: 
            related_artists_links[2].find_element(by=By.XPATH, value= './/a')
            driver.execute_script("window.scrollTo(0, 0);")
            artists.append(related_artists_links[2].find_element(by=By.XPATH, value= './/span').get_attribute("textContent"))
            related_artists_links[2].find_element(by=By.XPATH, value= './/a').click()

        related_artists_links=driver.find_elements(by=By.XPATH, value= './/h3[@class="userBadge__username sc-type-light sc-text-secondary sc-text-h4"]')

        time.sleep(5)

        return driver
    
    def close(self,driver):
        driver.close()

    def get_imgs(self,image_save_dir,database_dir,timestamp): 
        with open(database_dir, 'r') as handle:
            parsed= json.load(handle)
            img_link_data=parsed['Details']['Image Link']
            img_link_lists= []
            i=0

            for link in img_link_data:
                img_link_lists.append(link)
                url= link.replace('"', "")
                url_new = url.replace("https","http")
                response= requests.get(url_new)
                if response.status_code:
                    fp=open(f'{image_save_dir}\\{timestamp}{i}.jpg','wb')
                    fp.write(response.content)
                    fp.close()
                i+=1



