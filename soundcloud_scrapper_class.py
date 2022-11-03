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
        initial_url = self.url 
        driver.get(initial_url)
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

    def search(self,driver):
        search_bar= driver.find_elements(by=By.XPATH, value='//*[@class="headerSearch__input sc-input g-all-transitions-300"]')
        search_bar[1].click()
        search_word = input("Which artist would you like info from?")
        search_bar[1].send_keys(search_word)
        time.sleep(1)
        search_bar[1].send_keys(Keys.RETURN)
        time.sleep(2)
        return search_word

    def get_artists_only(self, driver):
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
    
    def go_to_tracks_tab(self,driver):
        driver.current_url
        track_tag = driver.find_elements(by= By.XPATH, value='//*[@class="g-tabs-link"]')
        track_tag[1].click()
        time.sleep(5)

    def scroll_and_load(self,driver):
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

    def collect_element_ids(self,driver):
        driver.current_url
        # list of elements by unique ID/class.
        tracks_list = driver.find_elements(by=By.XPATH, value='//*[@class="sc-link-primary soundTitle__title sc-link-dark sc-text-h4"]')
        song_tags_list= driver.find_elements(by=By.XPATH, value='//a[@class="sc-tag soundTitle__tag sc-tag-small"]')
        ministats_list = driver.find_elements(by=By.XPATH, value='//span[@class="sc-ministats sc-ministats-small  sc-ministats-plays sc-text-secondary"]')
        cover_art_list= driver.find_elements(by=By.XPATH, value='//a[@class="sound__coverArt"]')
        return tracks_list,song_tags_list,ministats_list,cover_art_list

    def scrape_song_titles(self,tracks_list):
        # find title of song and add to list.
        songs=[]
        for track_atags in tracks_list[:-3]:
            song_title =track_atags.find_element(by=By.XPATH, value='.//span').get_attribute("textContent")
            songs.append(song_title)
        return songs

    def scrape_song_genre_tags(self,song_tags_list):
        # find song genre tags.
        genre_tags = []
        for song_tag in song_tags_list:
            genre_tag = song_tag.find_element(by=By.XPATH, value='.//span[@class="sc-truncate sc-tagContent"]').get_attribute("textContent")
            genre_tags.append(genre_tag)
        return genre_tags

    def scrape_song_num_of_times_played(self,ministats_list):
        # get number of times played for each song. 
        total_num_plays = []
        for stat in ministats_list[:-3]:
            num_plays = stat.find_element(by=By.XPATH, value='.//span[@aria-hidden="true"]').get_attribute("textContent")
            total_num_plays.append(num_plays)
        return total_num_plays

    def scrape_image_links(self,cover_art_list):
        # find image links for each song.
        images =[]
        for cover_art in cover_art_list:
            span_tag = cover_art.find_element(by=By.XPATH, value='.//span')
            tag_attribute =span_tag.get_attribute('style')
            span_tag.location_once_scrolled_into_view
            time.sleep(1)
            cover_art_url =re.search('"(.*?)"',tag_attribute)
            images.append(cover_art_url.group(0))
        return images

    def get_timestamp(self):
        timestamp_now = datetime.now()
        str_date_time = timestamp_now.strftime("%d%m%Y_%H%M%S_")  
        return str_date_time

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

    def make_data_folders(self,artist):
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


