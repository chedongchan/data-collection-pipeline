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

sys.path.append('..\\soundcloud')
from soundcloud_scrapper_class import Scrapper

class SoundCloudSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https:\\www.soundcloud.com")
        cookies = page.HomePage(self.driver)
        cookies.accept_cookies_element
        time.sleep(2)
        cookies.click_accept_button()
        time.sleep(2)

    @unittest.skip
    def test_print(self):
        print("I am being tested!")
        assert True
    @unittest.skip
    def test_correct_website(self):
        main_page = page.HomePage(self.driver)
        self.assertTrue(main_page.is_title_matches())
        time.sleep(2)
    @unittest.skip
    def test_homepage_search_bar(self):
        search_bar_search= page.HomePage(self.driver)
        search_bar_search.search_text_element = "Test Case"
        time.sleep(2)
        search_results_page= page.ResultsPage(self.driver)
        self.assertTrue(search_results_page.is_results_found(), "No results found.")
    @unittest.skip
    def test_results_page_search_bar(self):
        results_page_search = page.ResultsPage(self.driver)
        results_page_search.results_page_search_element = "klasjklhqwbglbwjkbvlqk"
        time.sleep(2)
        search_results_page= page.ResultsPage(self.driver)
        self.assertTrue(search_results_page.is_results_found(), "No results found.")

    def test_list_generation(self):
        lists = Scrapper()
        tracks_list,song_tags_list,ministats_list,cover_art_list = lists.collect_element_ids(self.driver)
        self.assertTrue(type(tracks_list) == list)
        self.assertTrue(type(song_tags_list) == list) 
        self.assertTrue(type(ministats_list) == list) 
        self.assertTrue(type(cover_art_list ) == list)
        return tracks_list,song_tags_list,ministats_list,cover_art_list

    def test_json_file(self):
        data = Scrapper()
        data_collection = data.test_list_generation()
        data_collection.generate_database(data_collection)
        self.assertTrue(type(data_collection))
    
    def parse(filename): 
        try: 
            with open(filename) as f: 
                return json.load(f) 
        except ValueError as e: 
            print('invalid json: %s' % e) 
            return None
    
    def tearDown(self):
        # self.driver.close()
        pass
    
if __name__ == "__main__":
    unittest.main()
