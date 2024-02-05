from dataclasses import dataclass
import logging
import concurrent.futures
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from threading import current_thread
from app.services.house import HouseService
from app.utils.mongodb import close_mongodb_connection, connect_to_mongodb
from selenium.webdriver.chrome.service import Service
import os

CHROMEDRIVER_DIR = os.getenv("CHROMEDRIVER_DIR")
DRIVER_PATH = os.path.join(CHROMEDRIVER_DIR, "chromedriver")

logger = logging.getLogger(__name__)


@dataclass
class ThreadScraper:

    url: str = "https://www.hsbc.com.hk/zh-hk/mortgages/tools/property-valuation/"
    regions = []
    districts = []
    estates = []
    buildings = []
    floors = []
    blocks = []

    def __init__(self):
        retry = 0
        while retry < 10:
            try:
                connect_to_mongodb()
                logger.info("Connected to the MongoDB database!")
                self.root_browser = self.get_driver()
                time.sleep(2)
                self.house_service = HouseService()
                retry = 10
            except Exception:
                time.sleep(30)
                retry += 1

    def __enter__(self):
        return self

    def __exit__(self):
        close_mongodb_connection()
        logger.info('Close connection to Mongo DB.')

    def get_driver(self):
        retry = 0
        while retry < 10:
            try:
                options = Options()
                options.add_argument("--no-sandbox")
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--log-level=3")

                service = Service(executable_path=DRIVER_PATH)
                driver = webdriver.Chrome(
                    options=options,
                    # service=service
                )
                driver.get(self.url)
                retry = 10
            except Exception:
                time.sleep(20)
                retry += 1
        logger.info('HSBC Connected')
        return driver

    def scrape_districts(self):
        district_select = self.root_browser.find_element(
            by=By.ID, value="tools_form_2_selectized")
        district_select.click()
        time.sleep(0.5)
        self.districts = self.root_browser.find_element(
            by=By.ID, value="tools_form_2_menu").find_elements(by=By.TAG_NAME, value="div")
        district_select.click()

    def scrape_regions(self):
        regions_select = self.root_browser.find_element(
            by=By.ID, value="tools_form_1_selectized")
        regions_select.click()
        time.sleep(0.5)
        self.regions = self.root_browser.find_element(
            by=By.ID, value="tools_form_1_menu").find_elements(by=By.TAG_NAME, value="div")
        regions_select.click()

    def scrape_estates(self):
        estates_select = self.root_browser.find_element(
            by=By.ID, value="tools_form_3_selectized")
        estates_select.click()
        time.sleep(0.5)
        self.estates = self.root_browser.find_element(
            by=By.ID, value="tools_form_3_menu").find_elements(by=By.TAG_NAME, value="div")
        estates_select.click()

    def scrape_buldings(self):
        buildings_select = self.root_browser.find_element(
            by=By.ID, value="tools_form_4_selectized")
        buildings_select.click()
        time.sleep(0.5)
        self.buildings = self.root_browser.find_element(
            by=By.ID, value="tools_form_4_menu").find_elements(by=By.TAG_NAME, value="div")
        buildings_select.click()

    def scrape_floors(self):
        floors_select = self.root_browser.find_element(
            by=By.ID, value="tools_form_5_selectized")
        floors_select.click()
        time.sleep(0.5)
        self.floors = self.root_browser.find_element(
            by=By.ID, value="tools_form_5_menu").find_elements(by=By.TAG_NAME, value="div")
        floors_select.click()

    def scrape_blocks(self):
        blocks_select = self.root_browser.find_element(
            by=By.ID, value="tools_form_6_selectized")
        blocks_select.click()
        time.sleep(0.5)
        self.blocks = self.root_browser.find_element(
            by=By.ID, value="tools_form_6_menu").find_elements(by=By.TAG_NAME, value="div")
        blocks_select.click()

    def click_field(self, field_idx, id, browser: webdriver.Chrome):
        retry = 1
        while retry < 5:
            try:
                browser.find_element(
                    by=By.ID, value=f"tools_form_{id}_selectized").click()
                time.sleep(0.5)
                browser.find_element(by=By.ID, value=f"tools_form_{id}_menu").find_elements(
                    by=By.TAG_NAME, value="div")[field_idx].click()
                retry = 5
            except Exception:
                time.sleep(2)
                retry += 1

    def valuation(self, region_idx, district_idx, estate_idx, building_idx, floor_idx, block_idx):
        big_retry = 0
        while big_retry < 10:
            try:
                browser = self.get_driver()
                logger.info(
                    f'Thread :{current_thread().name} - {region_idx}-{district_idx}-{estate_idx}-{building_idx}-{floor_idx}-{block_idx} - Start Valuation')
                self.click_field(field_idx=region_idx, id=1, browser=browser)
                self.click_field(field_idx=district_idx, id=2, browser=browser)
                self.click_field(field_idx=estate_idx, id=3, browser=browser)
                self.click_field(field_idx=building_idx, id=4, browser=browser)
                self.click_field(field_idx=floor_idx, id=5, browser=browser)
                self.click_field(field_idx=block_idx, id=6, browser=browser)

                valuation = ""
                retry = 1
                while retry < 10:
                    submit_button = browser.find_element(
                        By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[1]/div/div[7]/a')
                    submit_button.click()
                    time.sleep(5)
                    valuation = browser.find_element(
                        By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/span').text
                    if valuation == "":
                        retry += 1
                        time.sleep(10)
                    else:
                        # browser.save_screenshot(f"{region_idx}-{district_idx}-{estate_idx}-{building_idx}-{floor_idx}-{block_idx}.png")
                        retry = 10

                gross_floor_area = browser.find_element(
                    By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[3]/div[2]/span').text
                saleable_area = browser.find_element(
                    By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[4]/div[2]/span').text
                property_age = browser.find_element(
                    By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[5]/div[2]/span').text
                logger.info(
                    f'Thread :{current_thread().name} - {region_idx}-{district_idx}-{estate_idx}-{building_idx}-{floor_idx}-{block_idx} - Valuation: {valuation}')
                selected_region = browser.find_element(
                    by=By.ID, value="tools_form_1_selected_text").text
                selected_district = browser.find_element(
                    by=By.ID, value="tools_form_2_selected_text").text
                selected_estate = browser.find_element(
                    by=By.ID, value="tools_form_3_selected_text").text
                selected_building = browser.find_element(
                    by=By.ID, value="tools_form_4_selected_text").text
                selected_floor = browser.find_element(
                    by=By.ID, value="tools_form_5_selected_text").text
                selected_block = browser.find_element(
                    by=By.ID, value="tools_form_6_selected_text").text
                browser.close()
                browser.quit()
                self.house_service.update_house_hsbc({
                    "valuation": valuation,
                    "region": selected_region,
                    "district": selected_district,
                    "estate": selected_estate,
                    "building": selected_building,
                    "floor": selected_floor,
                    "block": selected_block,
                    "gross_floor_area": gross_floor_area,
                    "saleable_area": saleable_area,
                    "property_age": property_age,
                })
                big_retry = 10
                return
            except Exception as e:
                if big_retry == 10:
                    logger.error(
                        f'Thread :{current_thread().name} - {region_idx}-{district_idx}-{estate_idx}-{building_idx}-{floor_idx}-{block_idx} - Error: {e}')
                big_retry += 1
                time.sleep(20)

    def scrape(self, selected_region, selected_district):
        self.scrape_regions()
        region_idx = selected_region
        if region_idx > 0:
            self.click_field(field_idx=region_idx, id=1,
                             browser=self.root_browser)

            self.scrape_districts()
            district_idx = selected_district
            if district_idx > 0:
                self.click_field(field_idx=district_idx,
                                 id=2, browser=self.root_browser)

                self.scrape_estates()
                for estate_idx, estate in enumerate(self.estates):
                    if estate_idx > 0:

                        self.click_field(field_idx=estate_idx,
                                         id=3, browser=self.root_browser)

                        self.scrape_buldings()
                        for building_idx, building in enumerate(self.buildings):
                            if building_idx > 0:
                                self.click_field(
                                    field_idx=building_idx, id=4, browser=self.root_browser)

                                self.scrape_floors()
                                for floor_idx, floor in enumerate(self.floors):
                                    if floor_idx > 0:
                                        self.click_field(
                                            field_idx=floor_idx, id=5, browser=self.root_browser)

                                        self.scrape_blocks()
                                        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                                            for block_idx, block in enumerate(self.blocks):
                                                if block_idx > 0:
                                                    self.click_field(
                                                        field_idx=block_idx, id=6, browser=self.root_browser)
                                                    executor.submit(
                                                        self.valuation, region_idx, district_idx, estate_idx, building_idx, floor_idx, block_idx)
                                            executor.shutdown()
