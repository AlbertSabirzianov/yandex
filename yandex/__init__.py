"""
Модуль для получения URL изображений и статей
с поисковой системы Яндекс с помощью Selenium.
"""
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

Y_PICTURES_URL = "https://yandex.ru/images/search?from=tabbar&text=<q_text>"
Y_ARTICLES_URL = "https://yandex.ru/search/?text=<q_text>"
EXCLUDE_SUBSTRINGS = ["yandex", "dzen"]


class SDriver:
    """
    Контекстный менеджер для инициализации и корректного
    завершения работы Chrome WebDriver с настройками stealth.

    При входе в контекст (__enter__):
    - Создаёт экземпляр Chrome WebDriver с опциями:
        --no-sandbox: отключение песочницы (рекомендуется для некоторых окружений, например, Docker).
        --disable-dev-shm-usage: отключение использования /dev/shm (решает проблемы с памятью в контейнерах).
        --headless: запуск браузера в безголовом режиме (без GUI).
    - Применяет настройки stealth для маскировки автоматизации (установка языков, вендора, платформы и др.).
    - Переопределяет User-Agent через Chrome DevTools Protocol для имитации обычного браузера.
    - Возвращает объект драйвера для использования внутри блока with.

    При выходе из контекста (__exit__):
    - Корректно завершает работу драйвера, закрывая браузер.

    Использование:
        with SDriver() as driver:
            driver.get("https://example.com")
            # работа с драйвером

    Зависимости:
    - selenium
    - selenium_stealth
    - webdriver_manager
    """
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
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def get_picture_urls(q: str) -> list[str]:
    """
    Получает список URL изображений с Яндекс.Картинок по заданному поисковому запросу.

    Аргументы:
        q (str): поисковый запрос, который будет подставлен в URL поиска изображений.

    Возвращает:
        list[str]: список URL изображений, найденных на странице результатов поиска.

    Описание работы:
        - Создаёт экземпляр браузера с помощью контекстного менеджера SDriver.
        - Загружает страницу поиска изображений Яндекса с подставленным запросом.
        - Ожидает появления всех элементов изображений с CSS-классом "ImagesContentImage-Image".
        - Извлекает и возвращает список значений атрибута "src" у найденных элементов.
    """
    with SDriver() as driver:
        driver.get(Y_PICTURES_URL.replace("<q_text>", q))
        img_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.ImagesContentImage-Image"))
        )
        return [e.get_attribute("src") for e in img_elements]


def get_articles_urls(q: str) -> list[str]:
    """
    Получает список URL статей с Яндекса по заданному поисковому запросу,
    исключая ссылки с определёнными подстроками.

    Аргументы:
        q (str): поисковый запрос, который будет подставлен в URL поиска статей.

    Возвращает:
        list[str]: список URL статей, отфильтрованных по исключаемым подстрокам (например, "yandex", "dzen").

    Описание работы:
        - Создаёт экземпляр браузера с помощью контекстного менеджера SDriver.
        - Загружает страницу поиска Яндекса с подставленным запросом.
        - Выполняет JavaScript для скрытия модального окна с классом "DistributionSplashScreenModalScene",
         если оно присутствует.
        - Ожидает появления всех ссылок с CSS-классом "Link organic__greenurl".
        - Извлекает href всех найденных ссылок.
        - Фильтрует список, исключая URL,
         содержащие подстроки из глобального списка EXCLUDE_SUBSTRINGS (без учёта регистра).
        - Возвращает отфильтрованный список URL.
    """
    with SDriver() as driver:
        driver.get(Y_ARTICLES_URL.replace("<q_text>", q))
        input_el = driver.find_element(By.CSS_SELECTOR, "input")
        driver.execute_script(
        """
        let el = document.querySelector('.DistributionSplashScreenModalScene');
        if (el) {
            el.style.display = 'none';
        }
        """
        )
        input_el.click()
        a_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.Link.organic__greenurl"))
        )
        urls = [a.get_attribute("href") for a in a_elements]
        return [
            s for s in urls
            if not any(sub in s.lower() for sub in EXCLUDE_SUBSTRINGS)
        ]

