from dataclasses import dataclass
import random
from threading import current_thread
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import logging
import concurrent.futures
from app.services.house import HouseService

from app.utils.mongodb import close_mongodb_connection, connect_to_mongodb

logger = logging.getLogger(__name__)


@dataclass
class TestScraper:

    broswer: webdriver.Chrome = None

    estates = []
    buildings = []
    floors = []
    blocks = []

    house_service = HouseService()

    def __exit__(self):
        close_mongodb_connection()
        logger.info('Close connection to Mongo DB.')

    def click_field(self, field_idx, id, browser: webdriver.Chrome):
        retry = 1
        while retry < 10:
            try:
                browser.find_element(
                    by=By.ID, value=f"tools_form_{id}_selectized").click()
                time.sleep(1)
                browser.find_element(by=By.ID, value=f"tools_form_{id}_menu").find_elements(
                    by=By.TAG_NAME, value="div")[field_idx].click()
                time.sleep(1)
                selected_text = browser.find_element(
                            by=By.ID, value=f"tools_form_{id}_selected_text").text
                if selected_text == None or selected_text == 'None':
                    raise Exception("Selected Text is Null")
                else:
                    return selected_text
            except Exception:
                time.sleep(30)
                retry += 1
        return ""

    def open_browser(self):
        max_retries = 100
        retries = 0
        browser = None
        while retries < max_retries:
            try:
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
                time.sleep(10)
                logger.debug(browser.title)

                connect_to_mongodb()
                logger.info("Connected to the MongoDB database!")
                return browser
            except Exception as e:
                browser.close()
                browser.quit()
                logger.warning(f"Something crash occurred. Retrying... ({retries+1}/{max_retries}), Error: f{e}")
                retries += 1
                time.sleep(random.uniform(10, 20))
        raise Exception("Failed after multiple retries")


    def scrape_estates(self,browser:webdriver.Chrome):
        estates_select = browser.find_element(
            by=By.ID, value="tools_form_3_selectized")
        estates_select.click()
        time.sleep(0.5)
        self.estates = browser.find_element(
            by=By.ID, value="tools_form_3_menu").find_elements(by=By.TAG_NAME, value="div")
        estates_select.click()

    def scrape_buldings(self,browser:webdriver.Chrome):
        buildings_select = browser.find_element(
            by=By.ID, value="tools_form_4_selectized")
        buildings_select.click()
        time.sleep(0.5)
        self.buildings = browser.find_element(
            by=By.ID, value="tools_form_4_menu").find_elements(by=By.TAG_NAME, value="div")
        buildings_select.click()

    def scrape_floors(self,browser:webdriver.Chrome):
        floors_select = browser.find_element(
            by=By.ID, value="tools_form_5_selectized")
        floors_select.click()
        time.sleep(0.5)
        self.floors = browser.find_element(
            by=By.ID, value="tools_form_5_menu").find_elements(by=By.TAG_NAME, value="div")
        floors_select.click()

    def scrape_blocks(self,browser:webdriver.Chrome):
        blocks_select = browser.find_element(
            by=By.ID, value="tools_form_6_selectized")
        blocks_select.click()
        time.sleep(0.5)
        self.blocks = browser.find_element(
            by=By.ID, value="tools_form_6_menu").find_elements(by=By.TAG_NAME, value="div")
        blocks_select.click()

    def valuation(self,browser:webdriver.Chrome,region_selected,district_selected,estate_selected,building_selected,floor_selected,block_selected):
        valuation = ""
        retry = 1
        while retry < 10:
            try:
                submit_button = browser.find_element(By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[1]/div/div[7]/a')
                submit_button.click()
                time.sleep(5)
                valuation = browser.find_element(By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/span').text
                if valuation == "":
                    raise Exception
                else:
                    # browser.save_screenshot(f"{region_idx}-{district_idx}-{estate_idx}-{building_idx}-{floor_idx}-{block_idx}.png")
                    retry = 10

                    gross_floor_area = browser.find_element(By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[3]/div[2]/span').text
                    saleable_area = browser.find_element(By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[4]/div[2]/span').text
                    property_age = browser.find_element(By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[5]/div[2]/span').text

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

    def scrape(self, selected_region, selected_district):
        retry = 0

     
        while retry<10:
            browser = self.open_browser()
            try:
                region_selected = self.click_field(field_idx=selected_region, id=1,
                                browser=browser)      
                time.sleep(2)
                district_selected = self.click_field(field_idx=selected_district, id=2,
                                browser=browser)   

                self.scrape_estates(browser=browser)
                estates_list = self.estates.pop(0)
                random.shuffle(estates_list)
                for estate_idx, estate in enumerate(estates_list):
                        estate_selected = self.click_field(field_idx=estate_idx,id=3, browser=browser)

                        self.scrape_buldings(browser=browser)
                        buildingss_list = self.buildings.pop(0)
                        random.shuffle(buildingss_list)
                        for building_idx, building in enumerate(buildingss_list):
                                building_selected = self.click_field(
                                        field_idx=building_idx, id=4, browser=browser)

                                self.scrape_floors(browser=browser)
                                floors_list = self.floors.pop(0)
                                random.shuffle(floors_list)
                                for floor_idx, floor in enumerate(floors_list):
                                        floor_selected = self.click_field(
                                                field_idx=floor_idx, id=5, browser=browser)

                                        self.scrape_blocks(browser=browser)
                                        blocks_list = self.blocks.pop(0)
                                        random.shuffle(blocks_list)
                                        for block_idx, block in enumerate(blocks_list):
                                                block_selected = self.click_field(
                                                            field_idx=block_idx, id=6, browser=browser)
                                                self.valuation(browser=browser,region_selected=region_selected, district_selected=district_selected, estate_selected=estate_selected, building_selected=building_selected,floor_selected=floor_selected,block_selected=block_selected)
                retry = 10
            except Exception as e:
                logger.warning(f"Something crash occurred. Error: f{e}")
                retry += 1
                time.sleep(2)
            finally:
                retry = 10
                logger.info('Closing Browser')
                browser.quit()

       
       
