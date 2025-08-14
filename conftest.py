import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="session")
def driver():
    """Chrome driver fixture for all tests"""
    options = Options()

    # HEADLESS rejim - CI muhitda kerak
    if os.getenv("HEADLESS", "1") in ("1", "true", "True"):
        options.add_argument("--headless=new")
        print("🤖 Running in HEADLESS mode")

    # CI muhitida kerakli flaglar
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")
    options.add_argument("--disable-javascript")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")

    # User data directory masalasini hal qilish
    import tempfile
    import uuid
    user_data_dir = os.path.join(tempfile.gettempdir(), f"chrome_user_data_{uuid.uuid4()}")
    options.add_argument(f"--user-data-dir={user_data_dir}")

    # Chrome service yaratish
    service = Service(ChromeDriverManager().install())

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        print("✅ Chrome driver successfully initialized")

        yield driver

    except Exception as e:
        print(f"❌ Chrome driver initialization failed: {e}")
        raise
    finally:
        if 'driver' in locals():
            driver.quit()
            print("🧹 Chrome driver closed")

        # Temporary user data directory'ni tozalash
        import shutil
        if os.path.exists(user_data_dir):
            try:
                shutil.rmtree(user_data_dir)
            except:
                pass