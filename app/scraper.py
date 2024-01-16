from dataclasses import dataclass
import time
from requests_html import HTML
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By


def get_user_agent():
    return UserAgent.random


@dataclass
class Scraper:
    url: str = "https://www.homepricehk.com/"
    driver: WebDriver = None
    html_obj: HTML = None

    def get_driver(self):
        if self.driver is None:
            user_agent = get_user_agent()
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument(f"user-agent={user_agent}")

            proxy_server_url = "20.111.54.16"
            options.add_argument(f'--proxy-server={proxy_server_url}')
            
            driver = webdriver.Chrome(
                options=options)
            self.driver = driver
        return self.driver

    def get(self):
        driver = self.get_driver()
        driver.get(self.url)
        driver.save_screenshot('start.png')
        return driver.page_source

    def get_html_obj(self):
        if self.html_obj is None:
            html_str = self.get()
            self.html_obj = HTML(html=html_str)
        return self.html_obj

    def get_region(self):
        region_select = Select(
            self.driver.find_element(by=By.ID, value="region"))
        for option in region_select.options:
            print(f'Region: {option.text}')
            option.click()
            self.get_district()

    def get_district(self):
        time.sleep(5)
        district_select = Select(
            self.driver.find_element(by=By.ID, value="district"))
        for option in district_select.options:
            print(f'District : {option.text}')
            option.click()
            self.get_estate()

    def get_estate(self):
        time.sleep(5)
        estate_select = Select(
            self.driver.find_element(by=By.ID, value="estate"))
        for option in estate_select.options:
            print(f'Estate : {option.text}')
            option.click()
            self.driver.save_screenshot(f'update.png')
            submit_button = self.driver.find_element(
                by=By.ID, value="estateSearch")
            submit_button.click()
            time.sleep(5)
            self.driver.save_screenshot(f'quotation.png')

    def scrape(self):
        self.get_html_obj()
        time.sleep(10)
        self.driver.save_screenshot(f'start.png')
        self.get_region()
        return {
            "html": ""
        }
