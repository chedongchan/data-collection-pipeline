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