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

app.send_task('scrape_house_property_value', args=(3, 2)) # 新界/離島 － 葵涌

app.send_task('scrape_house_property_value', args=(3, 3)) # 新界/離島 － 荔景

app.send_task('scrape_house_property_value', args=(3, 4)) # 新界/離島 － 大嶼山/離島

app.send_task('scrape_house_property_value', args=(3, 5)) # 新界/離島 － 馬鞍山

app.send_task('scrape_house_property_value', args=(3, 6)) # 新界/離島 － 西貢/清水灣
