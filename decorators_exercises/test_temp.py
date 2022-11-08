#Unit Testing Module
import unittest
from unittest.mock import patch
from temperature import Temperature


class TestTemp(unittest.TestCase):
    
    def setUp(self):
        print("setUp")
        self.temperature1 = Temperature(20)
        self.temperature2 = Temperature(-400)

    def tearDown(self):
        print("tearDown")
        pass

    def test_convert_to_fahrenheit(self):
        print("test_convert_to_fahrenheit")
        self.assertEqual(self.temperature1.convert_to_fahrenheit(),68)
        self.assertEqual(self.temperature2.convert_to_fahrenheit(),-688)
        
    def test_convert_to_celsius(self):
        print("test_convert_to_celsius")
        self.assertEqual(Temperature.convert_to_celsius(23),-5)
        self.assertEqual(Temperature.convert_to_celsius(32),0)
        self.assertEqual(Temperature.convert_to_celsius(401),205)        

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
    