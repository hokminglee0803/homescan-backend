from dataclasses import dataclass
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)


@dataclass
class TestScraper:

    broswer: webdriver.Chrome = None

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
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        browser = webdriver.Chrome(options=chrome_options)
        return browser

    @retry_on_crash
    def navigate_to_url(self,browser, url):
        browser.get(url)
        time.sleep(5)
        logger.debug(browser.title)
        return browser

    def scrape(self, selected_region, selected_district):
        url = "https://www.hsbc.com.hk/zh-hk/mortgages/tools/property-valuation/"

        browser = self.open_browser()
    
        try:
            browser = self.navigate_to_url(browser, url)

            self.click_field(field_idx=selected_region, id=1,
                             browser=browser)
        
            selected_region = browser.find_element(
                            by=By.ID, value="tools_form_1_selected_text").text
        
            logger.info(selected_region)

            time.sleep(3600)
        finally:
            browser.quit()

       
       
