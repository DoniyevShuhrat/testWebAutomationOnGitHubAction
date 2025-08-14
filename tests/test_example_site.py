from asyncio import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.example_page import ExamplePage

def test_title_is_example_domain():
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get("https://texnomart.uz")
        assert driver.title == "Texnomart.uz | Ўзбекистонда маиший техника ва электроника онлайн дўкони"
        sleep(5)
    finally:
        driver.quit()


# def test_more_information_navigates_to_more_info_page(driver):
#     page = ExamplePage(driver)
#     page.open()
#     page.click_more_info()
#     WebDriverWait(driver, 10).until(EC.title_is("Texnomart.uz"))
#     assert "Texnomart.uz" in driver.title