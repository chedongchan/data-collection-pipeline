from dataclasses import dataclass
import requests

class Temperature:
    '''
    This class is used to store and manipulates temperature values.

    Attributes:
        celsius (int): temperature value in Celsius
        fahrenheit (int): temperature value in Fahreneheit
    '''
    def __init__(self,celsius) -> None:
        '''
        Initialise an instance of Temperature class.
        Takes in Celsius integer value to begin.
        '''
        self.__celsius = celsius

    @property
    def celsius(self):
        print('Getting celsius value')
        return self.__celsius
    
    @celsius.setter
    def celsius(self,celsius):
        print("Setting celsius value")
        if self.check_temp(celsius):
            self.__celsius = celsius
    
    @celsius.deleter
    def celsius(self):
        print("Deleting celsius value")
        del self.__celsius

    def convert_to_fahrenheit(self) -> int:
        '''
        This function is used to convert temperature values from Celcius to Fahrenheit unit.

        Returns:
            fahrenheit: the temperature value in Fahrenheit units.
        '''
        celsius = self.celsius
        self.fahrenheit= celsius*1.8 + 32
        return self.fahrenheit

    @staticmethod
    def convert_to_celsius(f_temp) -> int:
        '''
        This static function is used to convert Fahrenheit temperature values to Celsius
        
        Args:
            f_temp (int): the temperature value in Fahrenheit units.

        Returns:
            (f_temp-32/)1.8 : the temperature value in Celsius units.
        '''
        return (f_temp-32)/1.8

    @staticmethod
    def check_temp(temperature) -> bool:
        '''
        This static function checks if the temperature in Celsius is within the range of -273 and 3000.

        Returns:
            bool: true or false value depending on the number.
        '''
        if temperature > -273 and temperature < 3000:
            return True
        else:
            return False

    @classmethod
    def fahrenheit_class_method(cls,f_temp):
        '''
        This class method creates a new instance of the Temperature class given a temperature in Fahrenheit.
        
        Args:
            f_temp (int): the temperature value in Fahrenheit units.

        Returns:
            f_temp: the temperature value in Fahrenheit units.
        '''
        return f_temp
        
    @classmethod
    def standard(cls):
        '''
        This class method creates a new instance of the Temperature and initialises c_temp attribute as 0.
        
        Returns:
            c_temp = the temperature value in Celsius units.
        '''
        c_temp = 0
        return c_temp

    def monthly_schedule(self):
        response =requests.get('https://www.youtube.com/watch?v=sugvnHA7ElY')
        if response.ok:
            return response.text
        else:
            return 'Bad Response!'

    @dataclass(order=True)
    class Temperature:
        def __init__(self,celsius):
            self.celsius = celsius
        def __eq__(self, other) -> bool:
            return False
        def __repr__(self,other) -> str:
            pass

    



    


    








        