import os
import pytest
import tempfile
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="session")
def driver():
    """Chrome driver fixture - GitHub Actions optimized"""
    options = Options()

    # GitHub Actions muhitini aniqlash
    is_github_actions = os.getenv("GITHUB_ACTIONS") == "true"
    is_headless = os.getenv("HEADLESS", "1") in ("1", "true", "True")

    if is_headless or is_github_actions:
        options.add_argument("--headless=new")
        print("🤖 Running in HEADLESS mode")

    # GitHub Actions uchun optimal flaglar
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")

    # Memory va performance optimization
    options.add_argument("--memory-pressure-off")
    options.add_argument("--max_old_space_size=4096")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-backgrounding-occluded-windows")

    # User data directory
    user_data_dir = os.path.join(tempfile.gettempdir(), f"chrome_user_data_{uuid.uuid4()}")
    options.add_argument(f"--user-data-dir={user_data_dir}")

    # Logging
    options.add_argument("--log-level=3")  # ERROR level only
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)

    driver = None
    try:
        if is_github_actions:
            # GitHub Actions muhitida
            print("🔧 GitHub Actions muhitida ishlayapman...")

            # WebDriverManager bilan sinab ko'ramiz
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                print("✅ WebDriverManager muvaffaqiyatli")
            except Exception as e:
                print(f"⚠️ WebDriverManager muammosi: {e}")
                # System ChromeDriver
                service = Service("/usr/local/bin/chromedriver")
        else:
            # Lokal muhit
            print("🏠 Lokal muhitda ishlayapman...")
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
            except:
                service = Service()  # PATH dan topadi

        # Driver yaratish
        driver = webdriver.Chrome(service=service, options=options)

        # Timeouts
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)

        print("✅ Chrome driver muvaffaqiyatli yaratildi")
        print(f"📍 Driver executable path: {service.path}")

        # Browser ma'lumotlari
        try:
            user_agent = driver.execute_script("return navigator.userAgent")
            print(f"🌐 User Agent: {user_agent[:100]}...")
        except:
            pass

        yield driver

    except Exception as e:
        print(f"❌ Chrome driver initialization failed: {e}")
        if driver:
            try:
                driver.quit()
            except:
                pass
        raise
    finally:
        # Cleanup
        if driver:
            try:
                driver.quit()
                print("🔒 Driver yopildi")
            except:
                pass

        # Temporary files tozalash
        try:
            import shutil
            shutil.rmtree(user_data_dir, ignore_errors=True)
        except:
            pass