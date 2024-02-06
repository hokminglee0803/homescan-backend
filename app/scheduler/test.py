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

    def retry_on_crash(func):
        def wrapper(*args, **kwargs):
            max_retries = 20
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Something crash occurred. Retrying... ({retries+1}/{max_retries})")
                    logger.warning(e)
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
        browser = webdriver.Remote(
            command_executor='http://18.141.147.24:4444/wd/hub',
            options=chrome_options
        )
        browser.get("https://www.hsbc.com.hk/zh-hk/mortgages/tools/property-valuation/")
        time.sleep(2)
        logger.debug(browser.title)
        return browser


    def scrape(self, selected_region, selected_district):

        browser = self.open_browser()

        try:
            selected_region_text = self.click_field(field_idx=selected_region, id=1,
                             browser=browser)      
            time.sleep(2)
            selected_district_text = self.click_field(field_idx=selected_district, id=2,
                             browser=browser)   
            logger.info(f'{selected_region_text} - {selected_district_text} ')
          
        finally:
            browser.quit()

       
       
