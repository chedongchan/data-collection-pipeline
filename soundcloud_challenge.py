from soundcloud_scrapper_class import Scrapper
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime

# Uses the __name__ == "__main__": conditional to run the script. 

if __name__ == "__main__":
    soundcloud = Scrapper()
    driver = soundcloud.load_and_accept_cookies()
    search_word = soundcloud.search(driver)
    soundcloud.filter_artist_results(driver)
    soundcloud.artist_home_page(driver)
    artists = [search_word]
    for i in range(int(input("number of related artists you would want data from?"))+1):
        soundcloud.go_to_tracks_page(driver)
        songs, genre_tags, total_num_plays, images =soundcloud.collect_data(driver)
        timestamp = str(soundcloud.get_timestamp())
        full_database= soundcloud.generate_database(artists[i],songs, genre_tags, total_num_plays, images,timestamp)
        artist_dir,image_save_dir = soundcloud.make_data_folder(artists[i])
        database_dir=soundcloud.save_dict_data_as_json(artists[i],full_database,artist_dir)
        soundcloud.get_imgs(image_save_dir,database_dir,timestamp)
        soundcloud.related_artists(driver,artists)
        i +=1

    soundcloud.close(driver)

