from dataclasses import dataclass
import time
from typing import List
from requests_html import HTML
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By


def get_user_agent():
    return UserAgent.random


class House:
    def __init__(self, region, district, estate):
        self.region = region
        self.district = district
        self.estate = estate


@dataclass
class Scraper:
    url: str = "https://www.homepricehk.com/"
    driver: WebDriver = None
    html_obj: HTML = None

    house = []

    def get_driver(self):
        if self.driver is None:
            user_agent = get_user_agent()
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument(f"user-agent={user_agent}")
            driver = webdriver.Chrome(
                options=options)
            self.driver = driver
        return self.driver

    def get(self):
        driver = self.get_driver()
        driver.get(self.url)
        return driver.page_source

    def get_html_obj(self):
        if self.html_obj is None:
            html_str = self.get()
            self.html_obj = HTML(html=html_str)
        return self.html_obj

    def get_region(self):
        region_select = Select(
            self.driver.find_element(by=By.ID, value="region"))
        for idx, option in enumerate(region_select.options):
            if idx > 0:
                temp_region_select = Select(
                    self.driver.find_element(by=By.ID, value="region"))
                temp_option = temp_region_select.options[idx]
                print(f'Region: {temp_option.text}')
                temp_option.click()
                self.get_district(region_idx=idx)

    def get_district(self, region_idx):
        time.sleep(5)
        district_select = Select(
            self.driver.find_element(by=By.ID, value="district"))
        for idx, option in enumerate(district_select.options):
            if idx > 0:
                temp_district_select = Select(
                    self.driver.find_element(by=By.ID, value="district"))
                temp_option = temp_district_select.options[idx]
                print(f'District : {temp_option.text}')
                temp_option.click()
                self.get_estate(region_idx=region_idx, district_idx=idx)

    def get_estate(self, region_idx, district_idx):
        time.sleep(5)
        estate_select = Select(
            self.driver.find_element(by=By.ID, value="estate"))
        for idx, option in enumerate(estate_select.options):
            if idx > 0:
                temp_estate_select = Select(
                    self.driver.find_element(by=By.ID, value="estate"))
                temp_option = temp_estate_select.options[idx]
                print(f'Estate : {temp_option.text}')
                temp_option.click()
                self.house.append(
                    House(region=region_idx, district=district_idx, estate=idx))

    def get_building(self):
        time.sleep(5)
        building_select = None
        try:
            building_select = Select(
                self.driver.find_element(by=By.ID, value="buildingSelect"))
            for idx, building in enumerate(building_select.options):
                if idx > 0:
                    temp_building_select = Select(
                        self.driver.find_element(by=By.ID, value="buildingSelect"))
                    temp_option = temp_building_select.options[idx]
                    print(f'Building : {temp_option.text}')
                    temp_option.click()
                    time.sleep(5)
                    self.get_quotation()
        except Exception as e:
            print('No Building Select')
            self.get_quotation()
        print('Finish Get Quote !')

    def get_quotation(self):
        time.sleep(5)
        table_data = {}

        table_1_element = self.driver.find_element(by=By.ID, value="table1")
        rows_1 = table_1_element.find_elements(by=By.TAG_NAME, value="tr")

        table_2_element = self.driver.find_element(by=By.ID, value="table2")
        rows_2 = table_2_element.find_elements(by=By.TAG_NAME, value="tr")

        for idx_1, row_1 in enumerate(rows_1):
            if idx_1 > 0 and idx_1 < len(rows_1)-1:
                floor = row_1.find_element(by=By.TAG_NAME, value="th")
                print(f'Floor : {floor.text}')
                for idx_2, row_2 in enumerate(rows_2):
                    if idx_2 == 0:
                        blook = row_2.find_element(by=By.TAG_NAME, value="th")
                        print(f'Block : {blook.text}')
                    elif idx_2 < len(rows_2)-1:
                        quotation = row_2.find_element(
                            by=By.TAG_NAME, value="a")
                        print(f'Price : {quotation.text}')
        return table_data

    def scrape(self):
        self.get_html_obj()
        time.sleep(10)
        self.get_region()
        for property in self.house:

            region_select = Select(
                self.driver.find_element(by=By.ID, value="region"))
            selected_region = region_select.options[property.region]

            selected_region.click()

            time.sleep(5)

            district_select = Select(
                self.driver.find_element(by=By.ID, value="district"))
            selected_district = district_select.options[property.district]

            selected_district.click()

            time.sleep(5)

            estate_select = Select(
                self.driver.find_element(by=By.ID, value="estate"))
            selected_estate = estate_select.options[property.estate]

            selected_estate.click()

            time.sleep(5)

            submit_button = self.driver.find_element(
                by=By.ID, value="estateSearch")
            submit_button.click()
            time.sleep(5)
            self.get_building()
            print('Wait...')
            time.sleep(60)
            self.get()
            time.sleep(10)

        return {
            "html": ""
        }
