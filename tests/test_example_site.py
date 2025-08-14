from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.example_page import ExamplePage

def test_title_is_example_domain(driver):
    page = ExamplePage(driver)
    page.open()
    assert driver.title == "Example Domain"

def test_more_information_navigates_to_more_info_page(driver):
    page = ExamplePage(driver)
    page.open()
    page.click_more_info()
    WebDriverWait(driver, 10).until(EC.title_is("More Information | Example Domain"))
    assert "IANA" in driver.title