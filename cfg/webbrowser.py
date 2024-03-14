from enum import Enum

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from cfg import osenv


class WebBrowserType(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"


class WebBrowser:

    # driver: webdriver = None

    def __init__(self, type_of_browser: WebBrowserType = WebBrowserType.CHROME, hidden: bool = False):
        self.type_of_browser = type_of_browser
        self.hidden = hidden

    def _open_chrome_browser(self):
        options = ChromeOptions()
        options.binary_location = osenv.get("WEBBROWSER_APP_PATH")
        options.add_argument("disable-infobars")
        options.add_experimental_option("detach", True)
        service = ChromeService(executable_path=osenv.get("WEBBROWSER_DRIVER_PATH"))
        if self.hidden:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=service, options=options)

    def _open_firefox_browser(self):
        options = FirefoxOptions()
        options.binary_location = osenv.get("WEBBROWSER_APP_PATH")
        service = FirefoxService(executable_path=osenv.get("WEBBROWSER_DRIVER_PATH"))
        if self.hidden:
            options.add_argument("--headless")
        self.driver = webdriver.Firefox(service=service, options=options)

    def open(self):
        if self.type_of_browser == WebBrowserType.CHROME:
            self._open_chrome_browser()
        if self.type_of_browser == WebBrowserType.FIREFOX:
            self._open_firefox_browser()

    def go_to(self, url: str):
        self.driver.get(url)

    def refresh(self):
        self.driver.refresh()

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()
