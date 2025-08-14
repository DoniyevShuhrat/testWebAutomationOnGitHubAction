from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ExamplePage:
    """Example page object for texnomart.uz"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        """Open the texnomart.uz homepage"""
        self.driver.get("https://texnomart.uz")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def click_more_info(self):
        """Click more info button - placeholder implementation"""
        # Bu method haqiqiy element topilganda to'ldiriladi
        print("🔍 Looking for more info element...")
        # Placeholder - haqiqiy elementni toping
        pass

    def get_title(self):
        """Get page title"""
        return self.driver.title