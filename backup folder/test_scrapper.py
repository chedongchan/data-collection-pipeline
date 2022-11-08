from soundcloud_scrapper_class import Scrapper
from unittest.mock import patch
import unittest


class TestScrapper(unittest.TestCase):
    
    def setUp(self):
        print("setUp")
        self.first_instance = Scrapper()

    def tearDown(self):
        print("tearDown")
        pass

    def test_load_and_accept_cookies(self):
        print("test load and accept cookies")
        self.assertEqual(type(self.first_instance.load_and_accept_cookies()), 'webdriver.Chrome')
           
        
    def test_search(self):
        print("test_convert_to_celsius")
        
    def test_monthly_schedule(self):
        with patch('temperature.requests.get') as mocked_get:
            mocked_get.return_value.ok = True 
            mocked_get.return_value.text = 'Success'

            schedule = self.temperature1.monthly_schedule()
            mocked_get.assert_called_with('https://www.youtube.com/watch?v=sugvnHA7ElY')
            self.assertEqual(schedule, 'Success')
          

            mocked_get.return_value.ok = False 

            schedule = self.temperature2.monthly_schedule()
            mocked_get.assert_called_with('https://www.youtube.com/watch?v=sugvnHA7ElY')
            self.assertEqual(schedule, 'Bad Response!')
    
        
    
if __name__ == '__main__':
    unittest.main()
    