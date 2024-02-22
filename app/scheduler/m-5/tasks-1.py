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

app.send_task('scrape_house_property_value', args=(5,2, [7,8,9,10,11])) # 九龍 － 紅磡

# app.send_task('scrape_house_property_value', args=(2, 4)) # 九龍 － 啟德

# app.send_task('scrape_house_property_value', args=(2, 5)) # 九龍 － 九龍灣

# app.send_task('scrape_house_property_value', args=(2, 6)) # 九龍 － 九龍城

# app.send_task('scrape_house_property_value', args=(2, 7)) # 九龍 － 九龍塘