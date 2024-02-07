import asyncio
from dataclasses import dataclass
import random
from threading import current_thread
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.services.house import HouseService

from app.utils.mongodb import close_mongodb_connection, connect_to_mongodb

logger = logging.getLogger(__name__)

WAIT_TIMEOUT = 10
@dataclass
class TestScraper:

    broswer: webdriver.Chrome = None

    estates = []
    buildings = []
    floors = []
    blocks = []

    house_service = HouseService()

    def click_field(self, field_idx, id, browser: webdriver.Chrome):
        retry = 1
        while retry < 10:
            try:
                WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, f"tools_form_{id}_selectized"))).click()

                WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, f"tools_form_{id}_menu"))).find_elements(
                    by=By.TAG_NAME, value="div")[field_idx].click()
                
                selected_text = WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, f"tools_form_{id}_selected_text"))).text
                if selected_text == None or selected_text == 'None':
                    raise Exception("Selected Text is Null")
                else:
                    return selected_text
            except Exception:
                time.sleep(30)
                retry += 1
        return ""

    def retry_on_crash(func):
        def wrapper(*args, **kwargs):
            max_retries = 100
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Something crash occurred. Retrying... ({retries+1}/{max_retries})")
                    retries += 1
                    time.sleep(random.uniform(10, 20))
            raise Exception("Failed after multiple retries")

        return wrapper

    @retry_on_crash
    async def open_browser(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--log-level=3")
        browser = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            options=chrome_options
        )
        browser.get("https://www.hsbc.com.hk/zh-hk/mortgages/tools/property-valuation/")
        time.sleep(2)
        logger.debug(browser.title)

        connect_to_mongodb()
        logger.info("Connected to the MongoDB database!")
        return browser

    def scrape_estates(self,browser:webdriver.Chrome):
        estates_select = WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, "tools_form_3_selectized")))
        estates_select.click()
        time.sleep(0.5)
        self.estates  = WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, "tools_form_3_menu"))).find_elements(by=By.TAG_NAME, value="div")
        estates_select.click()

    def scrape_buldings(self,browser:webdriver.Chrome):
        buildings_select = WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, "tools_form_4_selectized")))
        buildings_select.click()
        time.sleep(0.5)
        self.buildings = WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, "tools_form_4_menu"))).find_elements(by=By.TAG_NAME, value="div")
        buildings_select.click()

    def scrape_floors(self,browser:webdriver.Chrome):
        floors_select = WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, "tools_form_5_selectized")))
        floors_select.click()
        time.sleep(0.5)
        self.floors = WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, "tools_form_5_menu"))).find_elements(by=By.TAG_NAME, value="div")
        floors_select.click()

    def scrape_blocks(self,browser:webdriver.Chrome):
        blocks_select = WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, "tools_form_6_selectized")))
        blocks_select.click()
        time.sleep(0.5)
        self.blocks = WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, "tools_form_6_menu"))).find_elements(by=By.TAG_NAME, value="div")
        blocks_select.click()

    async def valuation(self,browser:webdriver.Chrome,region_selected,district_selected,estate_selected,building_selected,floor_selected,block_selected):
        valuation = ""
        retry = 1
        while retry < 10:
            try:
                submit_button = WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[1]/div/div[7]/a')))
                submit_button.click()
                time.sleep(5)
                valuation = WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/span'))).text
                if valuation == "":
                    raise Exception
                else:
                    # browser.save_screenshot(f"{region_idx}-{district_idx}-{estate_idx}-{building_idx}-{floor_idx}-{block_idx}.png")
                    retry = 10

                    gross_floor_area =WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[3]/div[2]/span'))).text
                    saleable_area = WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[4]/div[2]/span'))).text
                    property_age = WebDriverWait(browser, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[5]/div[2]/span'))).text

                    logger.info(f'{region_selected} - {district_selected} - {estate_selected} - {building_selected} - {floor_selected} - {block_selected}  --- Valuation: {valuation}')

                    self.house_service.update_house_hsbc({
                        "valuation": valuation,
                        "region": region_selected,
                        "district": district_selected,
                        "estate": estate_selected,
                        "building": building_selected,
                        "floor": floor_selected,
                        "block": block_selected,
                        "gross_floor_area": gross_floor_area,
                        "saleable_area": saleable_area,
                        "property_age": property_age,
                    })
            except:
                retry += 1
                time.sleep(10) 

    async def scrape(self, selected_region, selected_district):
        retry = 0
        browser = await self.open_browser()
        while retry<10:
            try:
                region_selected = self.click_field(field_idx=selected_region, id=1,
                                browser=browser)      
                time.sleep(2)
                district_selected = self.click_field(field_idx=selected_district, id=2,
                                browser=browser)   

                self.scrape_estates(browser=browser)
                for estate_idx, estate in enumerate(self.estates):
                    if estate_idx > 0:
                        estate_selected = self.click_field(field_idx=estate_idx,id=3, browser=browser)

                        self.scrape_buldings(browser=browser)
                        for building_idx, building in enumerate(self.buildings):
                            if building_idx > 0:
                                building_selected = self.click_field(
                                        field_idx=building_idx, id=4, browser=browser)

                                self.scrape_floors(browser=browser)
                                for floor_idx, floor in enumerate(self.floors):
                                    if floor_idx > 0:
                                        floor_selected = self.click_field(
                                                field_idx=floor_idx, id=5, browser=browser)

                                        self.scrape_blocks(browser=browser)
                                        for block_idx, block in enumerate(self.blocks):
                                            if block_idx > 0:
                                                block_selected = self.click_field(
                                                            field_idx=block_idx, id=6, browser=browser)
                                                await self.valuation(browser=browser,region_selected=region_selected, district_selected=district_selected, estate_selected=estate_selected, building_selected=building_selected,floor_selected=floor_selected,block_selected=block_selected)
                retry = 10
            except:
                retry += 1
                time.sleep(2)
            finally:
                browser.quit()
                close_mongodb_connection()
                logger.info('Close connection to Mongo DB.')

       
       
