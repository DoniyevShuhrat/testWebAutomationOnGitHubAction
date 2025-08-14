import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def driver():
    options = Options()
    # HEADLESS=1 bo'lsa headless rejim
    if os.getenv("HEADLESS", "1") in ("1", "true", "True"):
        options.add_argument("--headless=new")

    # CI muhitida kerakli flaglar:
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Selenium Manager avtomatik Chrome(CT) va driverni topadi
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    yield driver
    driver.quit()
