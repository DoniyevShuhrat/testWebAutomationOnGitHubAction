import os
import pytest
import tempfile
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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
    user_data_dir = os.path.join(tempfile.gettempdir(), f"chrome_user_data_{uuid.uuid4()}")
    options.add_argument(f"--user-data-dir={user_data_dir}")

    try:
        # ChromeDriverManager dan to'g'ri path olish
        driver_path = ChromeDriverManager().install()
        print(f"📍 ChromeDriver path: {driver_path}")

        # To'g'ri chromedriver faylini topish
        if os.path.isdir(driver_path):
            # Agar directory bo'lsa, ichidan chromedriver faylini topamiz
            for root, dirs, files in os.walk(driver_path):
                for file in files:
                    if file == 'chromedriver' or file.startswith('chromedriver'):
                        if not file.endswith('.chromedriver') and 'THIRD_PARTY' not in file:
                            driver_path = os.path.join(root, file)
                            break

        # Fayl mavjudligini va bajarilishini tekshirish
        if not os.path.exists(driver_path):
            raise Exception(f"ChromeDriver fayl topilmadi: {driver_path}")

        # Fayl ruxsatlarini o'rnatish
        os.chmod(driver_path, 0o755)
        print(f"✅ ChromeDriver tayyor: {driver_path}")

        # Chrome service yaratish
        service = Service(driver_path)

        # Driver yaratish
        driver = webdriver.Chrome(service=service, options=options)
        print("✅ Chrome driver muvaffaqiyatli yaratildi")

        yield driver

    except Exception as e:
        print(f"❌ Chrome driver initialization failed: {e}")
        raise
    finally:
        try:
            driver.quit()
            print("🔒 Driver yopildi")
        except:
            pass