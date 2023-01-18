SoundCloud Website Data Scraper using Selenium in Python.  Get names, durations, images, number of times played, and genre tags of your favourite artists and also the related artists recommended by SoundCloud. 

# Project Description

I believe everyone is analytical to some extent. The musicians who create wonderful music are likely to have good knowledge and understanding of their craft but perhaps an under-appreciated aspect could be their immense exposure to other artists that came before them. In short, they have more data of previous successors. One aspiring musican might take this idea further. They might want to know all the musical metrics that an artist has or even better, all artists that fit the musician's preferences. SoundCloud has these metrics but to gather all information would simply be impossible considering that there could be 100s to 1000s of artists with many songs published. Therefore, in this case, a web scraper can be utilised to create a database of all these useful metrics, fully automated so that the musician can spend the time to work on their craft in the meantime.  
  
skills used: python, selenium, docker, PIL, A/B testing and CI/CD 

## This project is part of the AiCore Data Science Specialisation Programme
I explain the challenges and hurdles that I faced throughout the Data Collection Pipeline using a milestone Q&A format.

Data Collection Pipeline Project 

## Milestone 1: Set up the environment.
Github repo created and updated.

## Milestone 2: Decide which website you are going to collect data from  -> SoundCloud

- Q: Can you think of any data that could be used to provide business value to them if it could be understood and modelled?
- A: Collect data on songs of a particular artist and the recommended artists' songs from SoundCloud.


## Milestone 3: Prototype finding the individual page for each entry

- Q: What have you developed within the environment?
- A: Create a Scrapper class that contain methods that utilises Selenium functions to interact and automate chrome abilities. 

- Q: What utilities have you learnt this time?
- A: I have learnt to bypass cookies, scroll the page, collect useful data from both IMDB and Zoopla by searching for relevant html tags. I could automate the process to collect information from 5 pages listing 25 properties per page. This was achieved using both BeautifulSoup and Selenium.

## Milestone 4: Retrieve data from details pages

- Q: What additional methods have you added and why?
- A: For this milestone, I used json, requests and PIL modules. JSON was used to save the large dictionary data into a more accessible .json file, which will be more useful in the future, especially when using the information across a network. It is the text-based way of representing JavaScript object literals. Requests module was used to push through the image links to 'get' the response, and subsequently access the contents of the link. PIL was used to open and save files as jpg. 


The script.
```Python
from soundcloud_scrapper_class import Scrapper
# Uses the __name__ == "__main__": conditional to run the script. 
if __name__ == "__main__":
    soundcloud = Scrapper()
    driver = soundcloud.load_and_accept_cookies()
    search_word = soundcloud.search(driver)
    soundcloud.get_artists_only(driver)
    soundcloud.artist_home_page(driver)
    artists = [search_word]
    for i in range(int(input("number of related artists you would want data from?"))+1):
        soundcloud.go_to_tracks_tab(driver)
        soundcloud.scroll_and_load(driver)
        tracks_list, song_tags_list, ministats_list, cover_art_list =soundcloud.collect_element_ids(driver)
        songs = soundcloud.scrape_song_titles(tracks_list)
        genre_tags = soundcloud.scrape_song_genre_tags(song_tags_list)
        total_num_plays = soundcloud.scrape_song_num_of_times_played(ministats_list)
        images = soundcloud.scrape_image_links(cover_art_list)
        timestamp = str(soundcloud.get_timestamp())
        full_database = soundcloud.generate_database(artists[i],songs, genre_tags, total_num_plays, images,timestamp)
        artist_dir,image_save_dir = soundcloud.make_data_folders(artists[i])
        database_dir = soundcloud.save_dict_data_as_json(artists[i],full_database,artist_dir)
        soundcloud.get_imgs(image_save_dir,database_dir,timestamp)
        soundcloud.related_artists(driver,artists)
        i +=1

    soundcloud.close(driver)

```
The Scrapper Class.

```python
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

```

## Milestone 5: Documenting and testing.

- Q: What additional methods have you added and why?
- A: For this milestone, I learnt how to test a script using the unittest module. I have added docstrings to methods and the type checks for each function to ensure that the next person using my script will understand what is the expected returned data type. I have refactored as much of each 'function' as possible to make each function simple and easy to debug in the future. Going through the list of optimisations, I have minimised the use of loops and cleaned up the imports to be in alphabetical order e.g.

- Q: What was difficult?
- A: Right now, the testing of my scraper outside of the class is a tricky concept to grasp. In the end, I realised that rather than actually testing the functionality of my script, I must check for elements outside of my control. For example, I need to see if that the website still IDs their searchbox with the name q e.g.

> main.py 
```Python
import unittest
from selenium import webdriver
import page
import time
import json
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

sys.path.append('..\\soundcloud')
from soundcloud_scrapper_class import Scrapper

class SoundCloudSearch(unittest.TestCase):
    #setup functions
    print("I am setting up the first few compulsory functions: headless, maximised window, implicit waits and accepting cookies so the driver can navigate the website freely.")
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--kiosk")
        cls.driver = webdriver.Chrome(chrome_options = chrome_options)
        cls.driver.get("https://www.soundcloud.com")
        cls.driver.implicitly_wait(10)
        cookies = page.HomePage(cls.driver)
        cookies.accept_cookies_element
        time.sleep(2)
        cookies.click_accept_button()
        time.sleep(2)

    def setUp(self):
        self.driver.implicitly_wait(10)

    def test_print(self):
        print("I am testing if test functions are being tested!")
        assert True
    
    def test_correct_website(self):
        print("I am testing if the driver is getting the right website with the word SoundCloud in the title.")
        self.driver.get("https:\\www.soundcloud.com")
        time.sleep(2)
        main_page = page.HomePage(self.driver)
        self.assertTrue(main_page.is_title_matches())
        time.sleep(2)
    
    def test_homepage_search_bar(self):
        print("I am testing if the search bar on the HomePage can be searched with the search text element.")
        self.driver.get("https:\\www.soundcloud.com")
        time.sleep(2)
        search_bar_search= page.HomePage(self.driver)
        search_bar_search.search_text_element = "Test Case"
        time.sleep(2)
        search_results_page= page.ResultsPage(self.driver)
        self.assertTrue(search_results_page.is_results_found(), "No results found.")
   
    def test_results_page_search_bar(self):
        print("I am testing if the search bar on the ResultsPage can be searched with the search text element.")
        self.driver.get("https:/soundcloud.com/search?q=test%20case")
        time.sleep(2)
        results_page_search = page.ResultsPage(self.driver)
        results_page_search.results_page_search_element = "klasjklhqwbglbwjkbvlqk"
        time.sleep(2)
        search_results_page= page.ResultsPage(self.driver)
        self.assertTrue(search_results_page.is_results_found(), "No results found.")

    def test_sidebar_elements(self):
        print("I am testing if the sidebar elements on the ResultsPage can be selected.")
        self.driver.get("https:/soundcloud.com/search?q=test%20case")
        time.sleep(2)
        sidebar = self.driver.find_element(by= By.XPATH, value= './/li[@class="g-nav-item g-nav-item-people searchOptions__navigation-people searchOptions__navigationItem sc-py-0.5x sc-px-2x sc-mb-0.5x"]')
        people_option = sidebar.find_element(by= By.XPATH, value= './/a')
        self.assertTrue(people_option.is_displayed())

    def test_song_elements(self):
        print("I am testing if elements of the track can be accessed from XPATH.")
        self.driver.get("https:/soundcloud.com/amalaofficial")
        time.sleep(2)
        tracks_list = self.driver.find_elements(by=By.XPATH, value='//*[@class="sc-link-primary soundTitle__title sc-link-dark sc-text-h4"]')
        self.assertTrue(type(tracks_list) ==list)
        song_tags_list= self.driver.find_elements(by=By.XPATH, value='//a[@class="sc-tag soundTitle__tag sc-tag-small"]')
        self.assertTrue(type(song_tags_list) ==list)
        ministats_list = self.driver.find_elements(by=By.XPATH, value='//span[@class="sc-ministats sc-ministats-small  sc-ministats-plays sc-text-secondary"]')
        self.assertTrue(type( ministats_list) ==list)
        cover_art_list= self.driver.find_elements(by=By.XPATH, value='//a[@class="sound__coverArt"]')
        self.assertTrue(type(cover_art_list) ==list)

    def test_tracks_tab_element(self):
        print("I am testing if the tracks tab on the ResultsPage can be selected when on a particular artist's content page.")
        self.driver.get("https:/soundcloud.com/amalaofficial")
        time.sleep(2)
        track_tag = self.driver.find_elements(by= By.XPATH, value='//*[@class="g-tabs-link"]')
        self.assertTrue(type(track_tag) ==list)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()
    
if __name__ == "__main__":
    unittest.main()

```

> page.py

```Python
from locator import MainPageLocator
from element import BasePageElement, CookiePageElement, SearchBarElement

class SearchTextElement(BasePageElement):
    locator = 'q'
class GoButtonElement(BasePageElement):
    locator = "go"
class CookiesAcceptElement(CookiePageElement):
    locator = 'onetrust-accept-btn-handler'
class SearchBarSearchElement(SearchBarElement):
    locator = 'q'

class BasePage(object):
    def __init__(self,driver):
        self.driver = driver

class HomePage(BasePage):
    accept_cookies_element = CookiesAcceptElement()
    search_text_element = SearchBarSearchElement()

    def is_title_matches(self):
        print(self.driver.title)
        return "SoundCloud" in self.driver.title

    def click_go_button(self):
        element = self.driver.find_element(*MainPageLocator.GO_BUTTON)
        element.click()
    
    def click_accept_button(self):
        print("accepting cookies")
        element = self.driver.find_element(*MainPageLocator.ACCEPT_BUTTON)
        element.click()
    
class ArtistPage(BasePage):
    pass

class ResultsPage(BasePage):

    def __init__(self,driver):
        self.driver = driver
        self.driver.get("https:\\soundcloud.com\\search?")
        print("driver set to results page...")

    results_page_search_element = SearchTextElement()
    
    def is_results_found(self):
        print("im checking if results are found in the results page.")
        return "No results found." not in self.driver.page_source

    def search_text(self):
        print("im searching via the text box")
        element = self.driver.find_element(*MainPageLocator.SEARCH_RESULTS_PAGE_SEARCH_BAR)
    
```
> element.py
```Python 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class BasePageElement(object):
    def __set__(self, obj, value):
        driver =obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(By.NAME, self.locator))
        driver.find_element(by=By.NAME,value =self.locator).clear()
        time.sleep(2)
        driver.find_element(by=By.NAME,value =self.locator).send_keys(value)
        time.sleep(2)

    def __get__(self, obj,owner):   
        driver = obj.driver
        WebDriverWait(driver,100).until(
            lambda driver: driver.find_element(by=By.NAME,value =self.locator))
        element=driver.find_element(by=By.NAME,value =self.locator)
        return element.get_attribute("value")

class CookiePageElement(object):
    def __set__(self, obj, value):
        driver =obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_elements(By.ID, self.locator))
        time.sleep(5)

    def __get__(self, obj,owner):   
        driver = obj.driver
        WebDriverWait(driver,100).until(
            lambda driver: driver.find_element(by=By.ID,value =self.locator))
        element=driver.find_element(by=By.ID,value =self.locator)
        return element.get_attribute("value")

class SearchBarElement(object):
    def __set__(self, obj, value):
        driver =obj.driver
        WebDriverWait(driver, 100).until(
             lambda driver: driver.find_elements(By.NAME, self.locator))[1]
        time.sleep(2)
        driver.find_elements(by=By.NAME,value =self.locator)[1].clear()
        time.sleep(2)
        driver.find_elements(by=By.NAME,value =self.locator)[1].send_keys(value)
        driver.find_elements(by=By.NAME,value =self.locator)[1].send_keys(Keys.RETURN)
        time.sleep(2)

    def __get__(self, obj,owner):   
        driver = obj.driver
        WebDriverWait(driver,100).until(
            lambda driver: driver.find_elements(by=By.NAME,value =self.locator))[1]
        element=driver.find_elements(by=By.NAME,value =self.locator)[1]
        return element.get_attribute("value")

```

> locator.py

```Python
from selenium.webdriver.common.by import By

class MainPageLocator(object):
    GO_BUTTON = (By.CLASS_NAME, "headerSearch__submit sc-ir")
    SEARCH_BAR = (By.NAME, "q")
    ACCEPT_BUTTON = (By.ID,'onetrust-accept-btn-handler')
    
class SearchResultsPageLocators(object):
    SEARCH_RESULTS_PAGE_SEARCH_BAR = (By.NAME, "q")

```


## Milestone 6: Containerising the scraper

- Q: What did you learn in this milestone? 
- A: I had to learn how to create a Docker image which would run my app in any OS - one of the benefits of using Docker. I had to learn some syntax for Ubuntu and Docker commands. 

- Q: What was difficult? 
- A: I initially thought that the task was to use the Remote Webdriver to essentially run my scraper in a virtual machine elsewhere setting up networks that depend on other docker containers. However, it was much simpler than that, where the task's focus was not that but instead to ensure I know how to containerise my app as a Dockerfile container and pushed to the hub, which can be pulled from any computer and be used in the local machine.

The below code 

```Dockerfile
# Specify image:tag
FROM python:3.9
RUN pip install --no-cache-dir --upgrade pip

# single line codes for RUN commands.

# Download and install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - &&\
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' &&\
    apt-get update && apt-get -y install google-chrome-stable

#Download and install ChromeDriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip &&\
    apt-get install -yqq unzip &&\
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Copy data from docker context
COPY . .

# Install the required modules for scraper.
RUN pip install -r scraper_docker_image/requirements.txt

# Afterwards, we run container with this command.
ENTRYPOINT ["python3", "scraper/main.py"]
```

In order for the selenium web scraper to work in all machines.. I had to change some lines of code in the scraper class file.

```python
class Scraper():
    def __init__(self) -> None:
            self.url = "https://www.soundcloud.com"
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--maximise")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument('no-sandbox') 
            chrome_options.add_argument("disable-dev-shm-usage")
            self.driver = webdriver.Chrome(ChromeDriverManager().install(),options = chrome_options)
```

In order to run the scraper in a docker container means that the scraper must run headless. Few other arguments were used to ensure that the script does not run into any errors such as maximising the window and disabling any notifications. Instead of hard-coding the directory of the webdriver executable, I used the ChromeDriverManager package to install the driver, automatically setting the chromedriver version to be the latest one.

## Milestone 7: Set up a CI/CD piperline for your Docker Image

- Q: What did you learn in this milestone? 
- A: I had to learn how to build and deploy my Docker image to Dockerhub with the aid of Github Actions. In order to do this, I had to set up Github secrets that authenticates communication between my dockerhub and github accounts. The github actions require a workflows main.yml file that instructs github to perform actions. In this case, everytime the repo is updated with a push commmand, it will login/check credentials, (re-)build the docker image and then push to dockerhub. As I push this updated README.md file, it will initiate the action.

```yaml 
name: soundcloud_scraper_docker_push

on:
  push:
    branches:
      - "main"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    -
      name: Checkout
      uses: actions/checkout@v3
    -
      name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_HUB_USERNAME }}
        password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}
    -
      name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    -
      name: Build and push
      uses: docker/build-push-action@v3
      with:
        context: .
        file: ./scraper_docker_image/Dockerfile
        push: true
        tags: ${{ secrets.DOCKER_HUB_USERNAME }}/soundcloud_scraper:finalversion
```
