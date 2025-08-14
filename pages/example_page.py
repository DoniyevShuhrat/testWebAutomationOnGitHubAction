from selenium.webdriver.common.by import By

class ExamplePage:
    URL = "https://texnomart.com"
    MORE_INFO = (By.CSS_SELECTOR, "a[href*='more-info']")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def click_more_info(self):
        self.driver.find_element(*self.MORE_INFO).click()