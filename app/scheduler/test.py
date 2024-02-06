from dataclasses import dataclass
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import logging
import concurrent.futures

logger = logging.getLogger(__name__)


@dataclass
class TestScraper:

    broswer: webdriver.Chrome = None
    estates = []
    buildings = []
    floors = []
    blocks = []

    def click_field(self, field_idx, id, browser: webdriver.Chrome):
        retry = 1
        while retry < 5:
            try:
                browser.find_element(
                    by=By.ID, value=f"tools_form_{id}_selectized").click()
                time.sleep(5)
                browser.find_element(by=By.ID, value=f"tools_form_{id}_menu").find_elements(
                    by=By.TAG_NAME, value="div")[field_idx].click()
                time.sleep(2)
                selected_text = browser.find_element(
                            by=By.ID, value=f"tools_form_{id}_selected_text").text
                if selected_text == None or selected_text == 'None':
                    raise Exception("Selected Text is Null")
                else:
                    return selected_text
            except Exception:
                time.sleep(2)
                retry += 1
        return ""

    def retry_on_crash(func):
        def wrapper(*args, **kwargs):
            max_retries = 20
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Page crash occurred. Retrying... ({retries+1}/{max_retries})")
                    retries += 1
                    time.sleep(random.uniform(30, 100))
            raise Exception("Failed after multiple retries")

        return wrapper

    @retry_on_crash
    def open_browser(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--log-level=3")
        # browser = webdriver.Chrome(options=chrome_options)
        browser = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            options=chrome_options
        )
        return browser
    

    @retry_on_crash
    def navigate_to_url(self,browser, url):
        browser.get(url)
        time.sleep(10)
        logger.debug(browser.title)
        return browser

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

    def scrape(self, selected_region, selected_district):
        url = "https://www.hsbc.com.hk/zh-hk/mortgages/tools/property-valuation/"

        browser = self.open_browser()
    
        try:
            browser = self.navigate_to_url(browser, url)
            selected_region = self.click_field(field_idx=selected_region, id=1,
                             browser=browser)      
            time.sleep(2)
            selected_district = self.click_field(field_idx=selected_district, id=2,
                             browser=browser)   
            self.scrape_estates(browser=browser)
            for estate_idx, estate in enumerate(self.estates):
                    if estate_idx > 0:
                        selected_estate = self.click_field(field_idx=estate_idx,
                                         id=3, browser=browser)
                        
                        self.scrape_buldings(browser=browser)
                        for building_idx, building in enumerate(self.buildings):
                            if building_idx > 0:
                                selected_building= self.click_field(
                                    field_idx=building_idx, id=4, browser=browser)

                                self.scrape_floors(browser=browser)
                                for floor_idx, floor in enumerate(self.floors):
                                    if floor_idx > 0:
                                        selected_floor = self.click_field(
                                            field_idx=floor_idx, id=5, browser=browser)

                                        self.scrape_blocks(browser=browser)
                                        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                                            for block_idx, block in enumerate(self.blocks):
                                                if block_idx > 0:
                                                    time.sleep(2)
                                                    selected_block = self.click_field(
                                                        field_idx=block_idx, id=6, browser=browser)
                                                    logger.info(f'{selected_region} - {selected_district} - {selected_estate} - {selected_building} - {selected_floor}- {selected_block}')
                                                    # executor.submit(
                                                    #     self.valuation, region_idx, district_idx, estate_idx, building_idx, floor_idx, block_idx)
                                            executor.shutdown()
                        
          


        finally:
            browser.quit()

       
       
