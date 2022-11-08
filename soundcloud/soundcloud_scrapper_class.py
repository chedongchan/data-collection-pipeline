from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from tkinter import image_names
import json
import os
import re
import requests
import time

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

    def search(self,driver: webdriver.Chrome) -> str:
        '''
        Clicks on search bar and inputs user's search terms then presses enter.
        
        Args:
            driver (webdriver.Chrome)

        Returns
        -------
        search_word (str): string variable of user's search term(s).

        '''
        search_bar= driver.find_elements(by=By.XPATH, value='//*[@class="headerSearch__input sc-input g-all-transitions-300"]')
        search_bar[1].click()
        search_word = input("Which artist would you like info from?")
        search_bar[1].send_keys(search_word)
        time.sleep(1)
        search_bar[1].send_keys(Keys.RETURN)
        time.sleep(2)
        return search_word

    def get_artists_only(self, driver):
        '''
        Filters the results page by showing artists only.
        
        Args:
            driver (webdriver.Chrome)
        '''
        driver.current_url
        sidebar_elements = driver.find_element(by= By.XPATH, value='//*[@class="searchOptions__container"]')
        sidebar = sidebar_elements.find_elements(by= By.XPATH, value= './/li')
        people_option = sidebar[3]
        people_option.click()
        time.sleep(2)
    
    def artist_home_page(self,driver):
        '''
        Clicks on the first artist on the artists results page and go to their home page.
        
        Args:
            driver (webdriver.Chrome)
        '''
        driver.current_url
        artist_tags = driver.find_element(by= By.XPATH, value='//*[@class="sc-media-content"]')
        artist_link = artist_tags.find_element(by= By.XPATH, value= './/h2')
        artist_link_atag = artist_link.find_element(by= By.XPATH, value= './/a')
        artist_link_atag.click()
        time.sleep(2)
    
    def go_to_tracks_tab(self,driver):
        '''
        Clicks on the tracks tab on the artist's home page.
        
        Args:
            driver (webdriver.Chrome)
        '''
        driver.current_url
        track_tag = driver.find_elements(by= By.XPATH, value='//*[@class="g-tabs-link"]')
        track_tag[1].click()
        time.sleep(5)

    def scroll_and_load(self,driver):
        '''
        Scroll down the page and ensure that all content is loaded before collecting data.
        
        Parameters:
            scroll_pause_time (int): number of seconds before the next scroll execution so that content has enough time to load content. 
        
        Args:
            driver (webdriver.Chrome)
        '''
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

    def collect_element_ids(self,driver) -> tuple[list,list,list,list]:
        '''
        Creates a list of web elements for each desired property.
        
        Args:
            driver (webdriver.Chrome)
        
        Returns:
            tracks_list (list): a list of web elements that has child elements that has the title of the track. 
            songs_tags_list (list): a list of web elements that has child elements that has the genre tag of the track. 
            ministats_list (list): a list of web elements that has child elements that has the number of times played statistics of the track. 
            cover_art_list (list): a list of web elements that has child elements that has the image link of the track. 
        '''

        driver.current_url
        # list of elements by unique ID/class.
        tracks_list = driver.find_elements(by=By.XPATH, value='//*[@class="sc-link-primary soundTitle__title sc-link-dark sc-text-h4"]')
        song_tags_list= driver.find_elements(by=By.XPATH, value='//a[@class="sc-tag soundTitle__tag sc-tag-small"]')
        ministats_list = driver.find_elements(by=By.XPATH, value='//span[@class="sc-ministats sc-ministats-small  sc-ministats-plays sc-text-secondary"]')
        cover_art_list= driver.find_elements(by=By.XPATH, value='//a[@class="sound__coverArt"]')
        return tracks_list,song_tags_list,ministats_list,cover_art_list

    def scrape_song_titles(self,tracks_list: list)-> list:
        '''
        Creates a list of song titles.
        
        Args:
            tracks_list (list): list of web element IDs that contains the track name
        
        Returns:
            songs (list): a list of titles of tracks. 
        '''

        # find title of song and add to list.
        songs=[]
        for track_atags in tracks_list[:-3]:
            song_title =track_atags.find_element(by=By.XPATH, value='.//span').get_attribute("textContent")
            songs.append(song_title)
        return songs

    def scrape_song_genre_tags(self,song_tags_list: list)-> list:
        '''
        Creates a list of genre tags of each song.
        
        Args:
            song_tags_list (list): list of web element IDs that contains the track music genre tags.
        
        Returns:
            genre_tags (list): a list of genre tags of tracks. 
        '''
        # find song genre tags.
        genre_tags = []
        for song_tag in song_tags_list:
            genre_tag = song_tag.find_element(by=By.XPATH, value='.//span[@class="sc-truncate sc-tagContent"]').get_attribute("textContent")
            genre_tags.append(genre_tag)
        return genre_tags

    def scrape_song_num_of_times_played(self,ministats_list: list)-> list:
        '''
        Creates a list of total number of played for each song.
        
        Args:
            ministats_list (list): list of web element IDs that contains total number played value for each song.
        
        Returns:
            ministats_list (list): a list of total number played of tracks. 
        '''
        # get number of times played for each song. 
        total_num_plays = []
        for stat in ministats_list[:-3]:
            num_plays = stat.find_element(by=By.XPATH, value='.//span[@aria-hidden="true"]').get_attribute("textContent")
            total_num_plays.append(num_plays)
        return total_num_plays

    def scrape_image_links(self,cover_art_list: list)-> list:
        '''
        Creates a list of cover art source URL of each song.
        
        Args:
            cover_art_list (list): list of web element IDs that contains the cover art URL link.
        
        Returns:
            images (list): a list of cover art URLs of each track. 
        '''
        # find image links for each song.
        images =[]
        for cover_art in cover_art_list:
            span_tag = cover_art.find_element(by=By.XPATH, value='.//span')
            tag_attribute =span_tag.get_attribute('style')
            span_tag.location_once_scrolled_into_view
            time.sleep(1)
            cover_art_url= re.search('"(.*?)"',tag_attribute)
            if cover_art_url is not None:
                images.append(cover_art_url.group(0))
        return images

    def get_timestamp(self) ->str:
        '''
        Prints the timestamp of the current call of function.
        
        Returns:
            str_date_time (str): string of timestamp in ddmmyy_hhmmss_ format.
        '''
        timestamp_now = datetime.now()
        str_date_time = timestamp_now.strftime("%d%m%Y_%H%M%S_")  
        return str_date_time

    def generate_database(self, artist:str, songs:list, genre_tags:list, total_num_plays:list,images:list,timestamp:str) -> dict:
        '''
        Creates a dictionary which is populated the name of the artist, timestamp of data scraping, and by lists of track names, genre tags, total number played and cover art URL links.
        
        Args:
            artist (str): string value of current artist, whom the data is scraped from.
            songs (list): a list of titles of tracks. 
            genre_tags (list): a list of genre tags of tracks. 
            images (list): a list of cover art URLs of each track.
            total_num_plays (list): a list of total number played of tracks.  
            timestamp (str): string of timestamp in ddmmyy_hhmmss_ format.

        Returns:
            full_database (dict): dictionary containing information scraped by the function.
        '''
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

    def make_data_folders(self,artist:str) ->tuple[str,str]:
        '''
        Creates folder for each artist where the raw data and images can be stored in.

        Args:
            artist (str): string text of current artist, whom the data is scraped from.
            
        Returns:
            artist_dir (str): string value of a directory, which is where the artist's folder is located
            image_save_dir (str): string value of 'images' folder directory, which is within the artist's folder and where images can be saved.
        '''
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
    
    def save_dict_data_as_json(self,artist:str,full_database:dict,artist_dir:str)->str:
        '''
        Saves the dictionary data into a json file in the artist's folder.

        Args:
            artist (str): string text of current artist, whom the data is scraped from.
            full_database (dict): dictionary containing information scraped by the function.
            artist_dir (str): string value of a directory, which is where the artist's folder is located
        
        Returns:
            database_dir (str): string text of json file directory.
        '''    
        with open(f'{artist_dir}\\{artist} soundcloud info.json','w') as fp:
            json.dump(full_database,fp,indent=4)
        database_dir =f'{artist_dir}\\{artist} soundcloud info.json'
        return database_dir
        
    def get_imgs(self,image_save_dir:str,database_dir:str,timestamp:str): 
        '''
        Opens the URL of each cover art, download, and saves the images to the images folder directory.

        Saves the file in timestamp format containing date, time and order of download.

        Args:
            image_save_dir (str): string value of 'images' folder directory, which is within the artist's folder and where images can be saved.
            database_dir (str): string text of json file directory.
            timestamp (str): string of timestamp in ddmmyy_hhmmss_ format.
        '''
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

    def related_artists(self, driver:webdriver.Chrome, hisotry_of_artists:list) -> webdriver.Chrome:
        '''
        Goes to the next artist home page by clicking one of the authors recommended by the SoundCloud recommendation engine, given that they have not been data scraped previously.

        Args:
           history_of_artists (list): a record of data scraped artists.

        Returns:
            driver (webdriver.Chrome): This driver is already in the SoundCloud webpage

        '''
        driver.current_url
        related_artists_links = driver.find_elements(by=By.XPATH, value= './/h3[@class="userBadge__username sc-type-light sc-text-secondary sc-text-h4"]')

        if related_artists_links[0] in hisotry_of_artists:
            related_artists_links[1].find_element(by=By.XPATH, value= './/a').get_attribute("href")
            driver.execute_script("window.scrollTo(0, 0);")
            hisotry_of_artists.append(related_artists_links[1].find_element(by=By.XPATH, value= './/span').get_attribute("textContent"))
            related_artists_links[1].find_element(by=By.XPATH, value= './/a').click()
        
        elif related_artists_links[1] not in hisotry_of_artists:
            related_artists_links[1].find_element(by=By.XPATH, value= './/a')
            driver.execute_script("window.scrollTo(0, 0);")
            hisotry_of_artists.append(related_artists_links[1].find_element(by=By.XPATH, value= './/span').get_attribute("textContent"))
            related_artists_links[1].find_element(by=By.XPATH, value= './/a').click()
            
        else: 
            related_artists_links[2].find_element(by=By.XPATH, value= './/a')
            driver.execute_script("window.scrollTo(0, 0);")
            hisotry_of_artists.append(related_artists_links[2].find_element(by=By.XPATH, value= './/span').get_attribute("textContent"))
            related_artists_links[2].find_element(by=By.XPATH, value= './/a').click()

        related_artists_links=driver.find_elements(by=By.XPATH, value= './/h3[@class="userBadge__username sc-type-light sc-text-secondary sc-text-h4"]')
        time.sleep(5)
        return driver
    
    def close(self,driver: webdriver.Chrome):
        '''
        Closes the driver. Thus terminating the window used for data scraping within this instance.
        
        '''
        driver.close()


