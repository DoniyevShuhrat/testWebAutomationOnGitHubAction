import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.example_page import ExamplePage


def test_title_is_example_domain(driver):
    """Test texnomart.uz title with proper fixture usage"""
    print("🧪 Starting title test...")

    # Navigate to the website
    driver.get("https://texnomart.uz")
    print(f"📍 Navigated to: {driver.current_url}")

    # Wait for page to load and get title
    WebDriverWait(driver, 10).until(
        lambda d: d.title != ""
    )

    actual_title = driver.title
    expected_title = "Texnomart.uz | Ўзбекистонда маиший техника ва электроника онлайн дўкони"

    print(f"📄 Page title: {actual_title}")
    print(f"🎯 Expected title: {expected_title}")

    # Assertion
    assert actual_title == expected_title, f"Title mismatch!\nActual: {actual_title}\nExpected: {expected_title}"

    print("✅ Title test passed!")

    # Small delay for stability (instead of sleep in async context)
    time.sleep(2)


def test_page_loads_successfully(driver):
    """Test that page loads without errors"""
    print("🧪 Testing page load...")

    driver.get("https://texnomart.uz")

    # Wait for page to be loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(("tag name", "body"))
    )

    # Check that we're on the right domain
    assert "texnomart.uz" in driver.current_url.lower()

    # Check that page title is not empty
    assert driver.title != ""

    print("✅ Page load test passed!")


@pytest.mark.skip(reason="Example page class needs to be implemented")
def test_more_information_navigates_to_more_info_page(driver):
    """Test navigation with ExamplePage - SKIPPED until page is implemented"""
    page = ExamplePage(driver)
    page.open()
    page.click_more_info()
    WebDriverWait(driver, 10).until(EC.title_contains("Texnomart.uz"))
    assert "Texnomart.uz" in driver.title