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
    
    