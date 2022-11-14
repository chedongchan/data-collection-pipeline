from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Remote("http://localhost:4444/wd/hub",
        options=chrome_options)
driver.get("https://www.soundcloud.com/")
print(driver.title)
