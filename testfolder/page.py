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
        return "No results found." not in self.driver.page_source

    def search_text(self):
        print("im searching via the text box")
        element = self.driver.find_element(*MainPageLocator.SEARCH_RESULTS_PAGE_SEARCH_BAR)
    
    

