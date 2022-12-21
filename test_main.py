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
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--kiosk")
        cls.driver = webdriver.Chrome(options = options)
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
