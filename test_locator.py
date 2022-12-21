from selenium.webdriver.common.by import By

class MainPageLocator(object):
    GO_BUTTON = (By.CLASS_NAME, "headerSearch__submit sc-ir")
    SEARCH_BAR = (By.NAME, "q")
    ACCEPT_BUTTON = (By.ID,'onetrust-accept-btn-handler')
    
class SearchResultsPageLocators(object):
    SEARCH_RESULTS_PAGE_SEARCH_BAR = (By.NAME, "q")


