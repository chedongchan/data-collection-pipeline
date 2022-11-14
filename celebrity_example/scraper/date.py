from datetime import datetime

class Date:
    '''
    This class is used to represent a date.

    Attributes:
        _day_of_month (tuple): The days in each month of the year
        _month_str = 
        year (int): The year of the date.
        month (int): The month of the date.
        day (int): The day of the date.
    '''
    _day_of_month = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    _month_str = ('January', 'February', 'March',
                  'April', 'May', 'June',
                  'July', 'August', 'September',
                  'October', 'November', 'December')

    def __init__(self, day: int, month: int, year: int):
        '''
        See help(Date) for accurate signature
        '''
        if not self.is_date_valid(day, month, year):
            raise ValueError('Date not valid')

        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        '''
        This function is used to return the string representation of the date.

        Returns:
            str: The string representation of the date.
        '''
        return "{0}-{1}-{2}".format(self.day, self.month, self.year)

    def __repr__(self):
        '''
        This function is used to return the string representation of the date.

        Returns:
            str: The string representation of the date.
        '''
        return "{0}-{1}-{2}".format(self.day, self.month, self.year)

    def __eq__(self, other):
        '''
        This function is used to compare the date with other date.

        Args:
            other (Date): The other date to be compared with.

        Returns:
            bool: True if the date is equal to the other date, False otherwise.
        '''
        return self.year == other.year and self.month == other.month and \
            self.day == other.day

    def __lt__(self, other):
        '''
        This function is used to compare the date with other date.

        Args:
            other (Date): The other date to be compared with.

        Returns:
            bool: True if the date is less than the other date, False otherwise.
        '''
        if self.year < other.year:
            return True
        elif self.year == other.year:
            if self.month < other.month:
                return True
            elif self.month == other.month:
                if self.day < other.day:
                    return True
        return False

    @staticmethod
    def is_leap_year(year: int) -> bool:
        '''
        This method checks if a year is a leap year

        Args:
            year (int): The year to check
        Returns:
            (bool): True if the year is a leap year, False otherwise
        '''
        return year % 4 == 0

    def is_date_valid(self, day: int, month: int, year: int) -> bool:
        '''
        This method is used to check if the date is valid.

        Args:
            day (int): The day of the date.
            month (int): The month of the date.
            year (int): The year of the date.

        Returns:
            bool: True if the date is valid, False otherwise.
        '''
        current_day = self._day_of_month[month - 1]
        if self.is_leap_year(year) and month == 2:
            current_day += 1

        return year >= 0 and month >= 1 and month <= 12 and \
            day >= 1 and day <= current_day

    @classmethod
    def from_string(cls, date_as_string):
        '''
        This function is used to create a date from a string.

        Args:
            date_as_string (str): The string representation of the date.

        Returns:
            Date: The date created from the string.
        '''
        day, month, year = map(int, date_as_string.split('-'))
        return cls(day, month, year)

    @classmethod
    def today(cls):
        '''
        This function is used to create a date from a string.

        Args:
            date_as_string (str): The string representation of the date.

        Returns:
            Date: The date created from the string.
        '''
        cur_day = datetime.now()
        day, month, year = cur_day.day, cur_day.month, cur_day.year
        return cls(day, month, year)

    def to_wiki_format(self):
        '''
        Returns the date into a format legible by the Wikipedia URL

        Returns:
            (str): String that can be appended to the Wikipedia URL
                   For example 'July_31'
        '''
        return f'{self._month_str[self.month - 1]}_{self.day}'