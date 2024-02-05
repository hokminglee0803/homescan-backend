from dataclasses import dataclass
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

logger = logging.getLogger(__name__)


@dataclass
class TestScraper:

    def scrape(self, selected_region, selected_district):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 如果不需要顯示瀏覽器視窗，可以加上此行設定
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get("https://www.hsbc.com.hk/zh-hk/mortgages/tools/property-valuation/")  # 替換為您想要打開的網址
        # 在這裡執行您的網頁操作
        time.sleep(5)  # 簡單示範等待 5 秒
        logger.info(driver.title)
        driver.quit()
       
