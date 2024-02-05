from dataclasses import dataclass
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import logging

logger = logging.getLogger(__name__)


@dataclass
class TestScraper:

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")  
    broswer = webdriver.Chrome(options=chrome_options)

    def click_field(self, field_idx, id, broswer: webdriver.Chrome):
        retry = 1
        while retry < 5:
            try:
                broswer.find_element(
                    by=By.ID, value=f"tools_form_{id}_selectized").click()
                time.sleep(0.5)
                broswer.find_element(by=By.ID, value=f"tools_form_{id}_menu").find_elements(
                    by=By.TAG_NAME, value="div")[field_idx].click()
                retry = 5
            except Exception:
                time.sleep(2)
                retry += 1

    def retry_on_crash(self,func):
        def wrapper(*args, **kwargs):
            max_retries = 3
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except WebDriverException as e:
                    print(f"Page crash occurred. Retrying... ({retries+1}/{max_retries})")
                    self.broswer.refresh()
                    retries += 1
            raise Exception("Failed after multiple retries")
        return wrapper

    @retry_on_crash
    def scrape(self, selected_region, selected_district):

        self.broswer.get("https://www.hsbc.com.hk/zh-hk/mortgages/tools/property-valuation/") 

        time.sleep(5)  

        logger.info(self.broswer.title)

        # self.click_field(field_idx=selected_region, id=1,
        #                      broswer=broswer)
        
        # selected_region = broswer.find_element(
        #                     by=By.ID, value="tools_form_1_selected_text").text
        
        # logger.info(selected_region)

        self.broswer.quit()
       
