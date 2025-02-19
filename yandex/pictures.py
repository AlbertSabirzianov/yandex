import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Y_URL = "https://yandex.ru/images/search?from=tabbar&text=<q_text>"


class SDriver:
    def __enter__(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Windows",
            webgl_vendor="Google Inc.",
            render="WebKit",
            fix_hairline=True
        )
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def get_picture(q: str) -> bytes:
    with SDriver() as driver:
        driver.get(Y_URL.replace("<q_text>", q))
        img_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img.ImagesContentImage-Image"))
        )
        img_url = img_element.get_attribute("src")
    response = requests.get(img_url)
    return response.content






