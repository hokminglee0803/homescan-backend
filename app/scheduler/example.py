from dataclasses import dataclass
import logging
import time
from requests_html import HTML
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from app.services.block import BlockService
from app.services.building import BuildingService
from app.services.district import DistrictService
from app.services.estate import EstateService
from app.services.floor import FloorService
from app.services.house import HouseService
from selenium.common.exceptions import NoSuchElementException

from app.services.region import RegionService
from app.utils.mongodb import close_mongodb_connection, connect_to_mongodb
import concurrent.futures
import threading

logger = logging.getLogger(__name__)

@dataclass
class Example:
    url: str = "https://www.hsbc.com.hk/zh-hk/mortgages/tools/property-valuation/"
    html_obj: HTML = None

    region_service = None
    district_service = None
    estate_service = None
    building_service = None
    floor_service = None
    block_service = None
    house_service = None

    regions = []

    def __init__(self):
        # connect_to_mongodb()
        # logger.info('Connected to Mongo DB.')
        self.region_service = RegionService()
        self.district_service = DistrictService()
        self.estate_service = EstateService()
        self.building_service = BuildingService()
        self.floor_service = FloorService()
        self.block_service = BlockService()
        self.house_service = HouseService()

    def __enter__(self):
        return self

    # def __exit__(self):
        # close_mongodb_connection()
        # logger.info('Close connection to Mongo DB.')

    def get_driver(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--max-connections=10") 
        driver = webdriver.Chrome(
                options=options)
        driver.get(self.url)
        return driver    

    def click_form_select(self,browser,id):
        try:
            form_select = browser.find_element(by=By.ID, value=id)
            form_select.click()   
            time.sleep(1) 
        except:
            retries = 0
            while retries < 5:
                    try:
                        form_select = browser.find_element(by=By.ID, value=id)
                        form_select.click()   
                        time.sleep(1) 
                    except:
                        pass
                    retries += 1
                    time.sleep(2)

    def drop_down_list(self,browser,form_select_id, menu_id):
            try:
                self.click_form_select(browser=browser,id=form_select_id)
                return browser.find_element(by=By.ID, value=menu_id).find_elements(by=By.TAG_NAME,value="div")
            except:
                retries = 0
                while retries < 5:
                    try:
                        time.sleep(2)
                        self.click_form_select(id=form_select_id)
                        time.sleep(2)
                        return browser.find_element(by=By.ID, value=menu_id).find_elements(by=By.TAG_NAME,value="div")
                    except:
                        pass
                    retries += 1
                    time.sleep(2)
                return []
            
    def select_form_data(self,browser,id,index,selected_text_id):    
        drop_down = browser.find_element(by=By.ID, value=id).find_elements(by=By.TAG_NAME,value="div")
        drop_down[index].click()
        time.sleep(1) 
        return browser.find_element(by=By.ID, value=selected_text_id).text    

    def example(self,region_idx):
        if region_idx > 0:
            current_thread = threading.current_thread()
            browser = self.get_driver()
            self.drop_down_list(browser=browser,form_select_id='tools_form_1_selectized',menu_id='tools_form_1_menu')
            selected_region = self.select_form_data(browser=browser, id='tools_form_1_menu',index=region_idx,selected_text_id="tools_form_1_selected_text")
            logger.info(f'{current_thread.name} - Selected Region: {selected_region}')

            distrcts = self.drop_down_list(browser=browser,form_select_id='tools_form_2_selectized',menu_id='tools_form_2_menu')
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                [executor.submit(self.scrape_district,district_idx) for district_idx,district in enumerate(distrcts)]
            browser.close()
            browser.quit()

    def scrape_district(self,district_idx):
        if district_idx>0:
            current_thread = threading.current_thread()
            browser = self.get_driver()
            self.drop_down_list(browser=browser,form_select_id='tools_form_2_selectized',menu_id='tools_form_2_menu')
            selected_district = self.select_form_data(browser=browser, id='tools_form_2_menu',index=district_idx,selected_text_id="tools_form_2_selected_text")
            logger.info(f'{current_thread.name} - Selected Region: {selected_district}')
            browser.close()
            browser.quit()

    def valuation_scrape(self):
        browser = self.get_driver()
        regions = self.drop_down_list(browser=browser,form_select_id='tools_form_1_selectized',menu_id='tools_form_1_menu')
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            [executor.submit(self.example,region_idx) for region_idx,region in enumerate(regions)]
    
                                                            
    def scrape(self):
        logger.info('Start Scraping')
        self.valuation_scrape()
        
    
