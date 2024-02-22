import asyncio
from celery import Celery
from celery.schedules import crontab
import app.config
from app.scheduler.test import TestScraper
settings = app.config.get_settings()

app = Celery(
    __name__, broker=f"{settings.redis_url}/0", backend=f"{settings.redis_url}/1"
)

@app.task(name='scrape_house_property_value')
def scrape_house_property_value(region, district):
    s = TestScraper()
    s.scrape(selected_region=region,selected_district=district)
    del s

app.send_task('scrape_house_property_value', args=(10,3, [11,12,13,14,15])) # 新界/離島 － 深井/青龍頭

# app.send_task('scrape_house_property_value', args=(3, 8)) # 新界/離島 － 沙田

# app.send_task('scrape_house_property_value', args=(3, 9)) # 新界/離島 － 上水

# app.send_task('scrape_house_property_value', args=(3, 10)) # 新界/離島 － 大埔

# app.send_task('scrape_house_property_value', args=(3, 11)) # 新界/離島 － 將軍澳
