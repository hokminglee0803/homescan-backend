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

logger = logging.getLogger(__name__)

def get_user_agent():
    return UserAgent.random

@dataclass
class HSBCScraper:
    url: str = "https://www.hsbc.com.hk/zh-hk/mortgages/tools/property-valuation/"
    driver: WebDriver = None
    html_obj: HTML = None

    region_service = None
    district_service = None
    estate_service = None
    building_service = None
    floor_service = None
    block_service = None
    house_service = None

    def __init__(self):
        connect_to_mongodb()
        logger.info('Connected to Mongo DB.')
        self.region_service = RegionService()
        self.district_service = DistrictService()
        self.estate_service = EstateService()
        self.building_service = BuildingService()
        self.floor_service = FloorService()
        self.block_service = BlockService()
        self.house_service = HouseService()

    def __enter__(self):
        return self

    def __exit__(self):
        close_mongodb_connection()
        logger.info('Close connection to Mongo DB.')

    def get_driver(self):
        user_agent = get_user_agent()
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f"user-agent={user_agent}")
        # options.add_argument("--kiosk")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(
                options=options)
            
        self.driver = driver
            
        return self.driver

    def get(self):
        try:
            driver = self.get_driver()
            driver.get(self.url)
            return driver.page_source
        except:
            self.driver.save_screenshot(f'retry.png')
            retries = 0
            while retries < 5:
                    try:
                        driver = self.get_driver()
                        driver.get(self.url)
                        return driver.page_source
                    except:
                        pass
                    retries += 1
                    time.sleep(2)


    def get_html_obj(self):
        self.get()
        # self.html_obj = HTML(html=html_str)
        # return self.html_obj

    def click_form_select(self,id):
        try:
            form_select = self.driver.find_element(by=By.ID, value=id)
            form_select.click()   
            time.sleep(1) 
        except:
            self.driver.save_screenshot(f'{id}.png')
            retries = 0
            while retries < 5:
                    try:
                        form_select = self.driver.find_element(by=By.ID, value=id)
                        form_select.click()   
                        time.sleep(1) 
                    except:
                        pass
                    retries += 1
                    time.sleep(2)

    def select_form_data(self,id,index,selected_text_id):    
        drop_down = self.driver.find_element(by=By.ID, value=id).find_elements(by=By.TAG_NAME,value="div")
        drop_down[index].click()
        time.sleep(1) 
        return self.driver.find_element(by=By.ID, value=selected_text_id).text
    
    def select_form_data_retry(self, form_select_id, form_id, index,selected_text_id):
        try:
            return self.select_form_data(id=form_id,index=index,selected_text_id=selected_text_id)
        except:
            self.driver.save_screenshot(f'{form_select_id}_{form_id}_{index}_{selected_text_id}.png')
            retries = 0
            while retries < 5:
                try:
                    self.click_form_select(id=form_select_id)
                    time.sleep(5)
                    return self.select_form_data(id=form_id,index=index,selected_text_id=selected_text_id)
                except:
                    pass
                retries += 1
                time.sleep(2)
            return ''
        
    def drop_down_list(self,form_select_id, menu_id):
        try:
            self.click_form_select(id=form_select_id)
            return self.driver.find_element(by=By.ID, value=menu_id).find_elements(by=By.TAG_NAME,value="div")
        except:
            retries = 0
            while retries < 5:
                try:
                    time.sleep(2)
                    self.click_form_select(id='tools_form_6_selectized')
                    time.sleep(2)
                    return self.driver.find_element(by=By.ID, value=menu_id).find_elements(by=By.TAG_NAME,value="div")
                except:
                    pass
                retries += 1
                time.sleep(2)
            return []

    def valuation(self,region,district,estate,building,floor,block):
        valuation = self.driver.find_element(By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/span').text
        gross_floor_area = self.driver.find_element(By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[3]/div[2]/span').text
        saleable_area = self.driver.find_element(By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[4]/div[2]/span').text
        property_age = self.driver.find_element(By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[2]/div/div[2]/div[5]/div[2]/span').text
        logger.info(f'Address: {region}{district}{estate}{building}{floor}{block}')
        logger.info(f'Valuation: {valuation}')
        logger.info(f'Gross Floor Area: {gross_floor_area}')
        logger.info(f'Saleable Area: {saleable_area}')
        logger.info(f'Property Age: {property_age}')
        # self.house_service.update_house_hsbc({
        #     "valuation": valuation,
        #     "region": region,
        #     "district": district,
        #     "estate": estate,
        #     "building": building,
        #     "floor": floor,
        #     "block": block,
        #     "gross_floor_area":gross_floor_area,
        #     "saleable_area":saleable_area,
        #     "property_age":property_age
        # })
    
    def example(document):
        print(document)

    def valuation_scrape(self,selected_region_idx,selected_distrcit_idx):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            [executor.submit(self.example, document) for document in [{1,1},{1,2},{1,3}]]
            # Select Region
            regions = self.drop_down_list(form_select_id='tools_form_1_selectized',menu_id='tools_form_1_menu')
            for region_idx,region in enumerate(regions):
                if region_idx == selected_region_idx: # Only Do the selected Region
                    if region_idx > 1:
                        self.click_form_select(id='tools_form_1_selectized')
                    selected_region = self.select_form_data(id='tools_form_1_menu',index=region_idx,selected_text_id="tools_form_1_selected_text")

                    # self.region_service.update_region(selected_region)

                    # Select District
                    districts = self.drop_down_list(form_select_id='tools_form_2_selectized',menu_id='tools_form_2_menu')

                    for district_idx,district in enumerate(districts):
                        if district_idx == selected_distrcit_idx :
                            # if district_idx > 1:
                            # Reclick Region
                            self.click_form_select(id='tools_form_1_selectized')
                            self.select_form_data_retry(form_select_id='tools_form_1_selectized',form_id='tools_form_1_menu',index=region_idx,selected_text_id="tools_form_1_selected_text")
                            # Reclick District
                            self.click_form_select(id='tools_form_2_selectized')
                            selected_district = self.select_form_data_retry(form_select_id='tools_form_2_selectized',form_id='tools_form_2_menu',index=district_idx,selected_text_id="tools_form_2_selected_text")

                            # self.district_service.update_district({
                            #     "name": selected_region,
                            #     "region": selected_district
                            # })

                            # Select Estate
                            estates = self.drop_down_list(form_select_id='tools_form_3_selectized',menu_id='tools_form_3_menu')

                            for estate_idx,estate in enumerate(estates):
                                if estate_idx > 0 :
                                    if estate_idx > 1:
                                        # Reclick Region
                                        self.click_form_select(id='tools_form_1_selectized')
                                        self.select_form_data_retry(form_select_id='tools_form_1_selectized',form_id='tools_form_1_menu',index=region_idx,selected_text_id="tools_form_1_selected_text")
                                        # Reclick District
                                        self.click_form_select(id='tools_form_2_selectized')
                                        self.select_form_data_retry(form_select_id='tools_form_2_selectized',form_id='tools_form_2_menu',index=district_idx,selected_text_id="tools_form_2_selected_text")
                                        # Reclick Estate
                                        self.click_form_select(id='tools_form_3_selectized')
                                    selected_estate= self.select_form_data_retry(form_select_id='tools_form_3_selectized',form_id='tools_form_3_menu',index=estate_idx,selected_text_id="tools_form_3_selected_text")

                                    # self.estate_service.update_estate({
                                    #     "name": selected_estate,
                                    #     "district": selected_district
                                    # })

                                    # Select Building
                                    buildings = self.drop_down_list(form_select_id='tools_form_4_selectized',menu_id='tools_form_4_menu')

                                    for building_idx,building in enumerate(buildings):
                                        if building_idx > 0 :
                                            if building_idx > 1:
                                                # Reclick Region
                                                self.click_form_select(id='tools_form_1_selectized')
                                                self.select_form_data_retry(form_select_id='tools_form_1_selectized',form_id='tools_form_1_menu',index=region_idx,selected_text_id="tools_form_1_selected_text")
                                                # Reclick District
                                                self.click_form_select(id='tools_form_2_selectized')
                                                self.select_form_data_retry(form_select_id='tools_form_2_selectized',form_id='tools_form_2_menu',index=district_idx,selected_text_id="tools_form_2_selected_text")
                                                # Reclick Estate
                                                self.click_form_select(id='tools_form_3_selectized')
                                                self.select_form_data_retry(form_select_id='tools_form_3_selectized',form_id='tools_form_3_menu',index=estate_idx,selected_text_id="tools_form_3_selected_text")
                                                # Reclick Building
                                                self.click_form_select(id='tools_form_4_selectized')
                                            selected_building = self.select_form_data_retry(form_select_id='tools_form_4_selectized',form_id='tools_form_4_menu',index=building_idx,selected_text_id="tools_form_4_selected_text")

                                            # self.building_service.update_building({
                                            #     "name": selected_building,
                                            #     "estate": selected_estate
                                            # })

                                            # Select Floor
                                            floors = self.drop_down_list(form_select_id='tools_form_5_selectized',menu_id='tools_form_5_menu')

                                            for floor_idx,floor in enumerate(floors):
                                                if floor_idx > 0 :
                                                    if floor_idx > 1:
                                                        # Reclick Region
                                                        self.click_form_select(id='tools_form_1_selectized')
                                                        self.select_form_data_retry(form_select_id='tools_form_1_selectized',form_id='tools_form_1_menu',index=region_idx,selected_text_id="tools_form_1_selected_text")
                                                        # Reclick District
                                                        self.click_form_select(id='tools_form_2_selectized')
                                                        self.select_form_data_retry(form_select_id='tools_form_2_selectized',form_id='tools_form_2_menu',index=district_idx,selected_text_id="tools_form_2_selected_text")
                                                        # Reclick Estate
                                                        self.click_form_select(id='tools_form_3_selectized')
                                                        self.select_form_data_retry(form_select_id='tools_form_3_selectized',form_id='tools_form_3_menu',index=estate_idx,selected_text_id="tools_form_3_selected_text")
                                                        # Reclick Building
                                                        self.click_form_select(id='tools_form_4_selectized')
                                                        self.select_form_data_retry(form_select_id='tools_form_4_selectized',form_id='tools_form_4_menu',index=building_idx,selected_text_id="tools_form_4_selected_text")
                                                        # Reclick Floor
                                                        self.click_form_select(id='tools_form_5_selectized')
                                                    selected_floor = self.select_form_data_retry(form_select_id='tools_form_5_selectized',form_id='tools_form_5_menu',index=floor_idx,selected_text_id="tools_form_5_selected_text")

                                                    # self.floor_service.update_floor({
                                                    #     "name": selected_floor,
                                                    #     "building": selected_building
                                                    # })

                                                    # Select Block
                                                    blocks =  self.drop_down_list(form_select_id='tools_form_6_selectized',menu_id='tools_form_6_menu')
                                                  
                                                    for block_idx,block in enumerate(blocks):
                                                        if block_idx > 0 :
                                                            if block_idx > 1:
                                                                # Reclick Region
                                                                self.click_form_select(id='tools_form_1_selectized')
                                                                self.select_form_data_retry(form_select_id='tools_form_1_selectized',form_id='tools_form_1_menu',index=region_idx,selected_text_id="tools_form_1_selected_text")
                                                                # Reclick District
                                                                self.click_form_select(id='tools_form_2_selectized')
                                                                self.select_form_data_retry(form_select_id='tools_form_2_selectized',form_id='tools_form_2_menu',index=district_idx,selected_text_id="tools_form_2_selected_text")
                                                                # Reclick Estate
                                                                self.click_form_select(id='tools_form_3_selectized')
                                                                self.select_form_data_retry(form_select_id='tools_form_3_selectized',form_id='tools_form_3_menu',index=estate_idx,selected_text_id="tools_form_3_selected_text")
                                                                # Reclick Building
                                                                self.click_form_select(id='tools_form_4_selectized')
                                                                self.select_form_data_retry(form_select_id='tools_form_4_selectized',form_id='tools_form_4_menu',index=building_idx,selected_text_id="tools_form_4_selected_text")
                                                                # Reclick Floor
                                                                self.click_form_select(id='tools_form_5_selectized')
                                                                self.select_form_data_retry(form_select_id='tools_form_5_selectized',form_id='tools_form_5_menu',index=floor_idx,selected_text_id="tools_form_5_selected_text")
                                                                # Reopen Block
                                                                self.click_form_select(id='tools_form_6_selectized')

                                                            selected_block = self.select_form_data_retry(form_select_id='tools_form_6_selectized',form_id='tools_form_6_menu',index=block_idx,selected_text_id="tools_form_6_selected_text")

                                                            # self.block_service.update_block({
                                                            #     "name": selected_block,
                                                            #     "floor": selected_floor,
                                                            #     "building": selected_building
                                                            # })

                                                            time.sleep(0.5)
                                                            submit_button = self.driver.find_element(By.XPATH, value='//*[@id="property-valuation-search"]/div[2]/form/div/div[2]/div[1]/div/div[7]/a')
                                                            submit_button.click()
                                                            time.sleep(2)

                                                            self.valuation(
                                                                region=selected_region,
                                                                district=selected_district,
                                                                estate=selected_estate,
                                                                building=selected_building,
                                                                floor=selected_floor,
                                                                block=selected_block
                                                            )

                                                            self.driver.delete_all_cookies()
                                                            self.driver.execute_script('localStorage.clear();')

                                                            self.driver.close()
                                                            self.driver.quit()
                                                            self.get_html_obj()
            
                                                            time.sleep(8)
                                                            self.driver.execute_script('window.scrollTo(0, 0);')
                                                            
    def scrape(self,selected_region_idx,selected_distrcit_idx):
        self.get_html_obj()
        time.sleep(2)

        self.valuation_scrape(selected_region_idx=selected_region_idx,selected_distrcit_idx=selected_distrcit_idx)

        time.sleep(5)
        
    
