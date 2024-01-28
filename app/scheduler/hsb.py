from dataclasses import dataclass
import logging
import time
from requests_html import HTML

from selenium.webdriver.chrome.webdriver import WebDriver
from app.services.building import BuildingService
from app.services.district import DistrictService
from app.services.estate import EstateService
from app.services.house import HouseService

from app.services.region import RegionService
from app.utils.mongodb import close_mongodb_connection, connect_to_mongodb

import undetected_chromedriver as uc

class House:
    def __init__(self, region, district, estate):
        self.region = region
        self.district = district
        self.estate = estate

logger = logging.getLogger(__name__)

@dataclass
class HSBScraper:
    url: str = "https://www.hsbc.com.hk/zh-hk/mortgages/tools/property-valuation/"
    driver: WebDriver = None
    html_obj: HTML = None

    house = []
    regions = []
    districts = []
    estates = []

    region_service = None
    district_service = None
    estate_service = None
    building_service = None
    house_service = None

    def __init__(self):
        connect_to_mongodb()
        logger.info('Connected to Mongo DB.')
        self.region_service = RegionService()
        self.district_service = DistrictService()
        self.estate_service = EstateService()
        self.building_service = BuildingService()
        self.house_service = HouseService()

    def __enter__(self):
        return self

    def __exit__(self):
        close_mongodb_connection()
        logger.info('Close connection to Mongo DB.')

    def get_driver(self):
        if self.driver is None:
            options = uc.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            driver = uc.Chrome(chrome_options=options)
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


    def scrape(self):
        self.get_html_obj()
        time.sleep(10)
    
