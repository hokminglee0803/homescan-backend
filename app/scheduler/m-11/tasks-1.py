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
def scrape_house_property_value(thread,region, district):
    s = TestScraper()
    s.scrape(thread_idx=thread,selected_region=region,selected_districts=district)
    del s

# app.send_task('scrape_house_property_value', args=(3, 12)) # 新界/離島 － 青衣

# app.send_task('scrape_house_property_value', args=(3, 13)) # 新界/離島 － 荃灣

# app.send_task('scrape_house_property_value', args=(3, 14)) # 新界/離島 － 屯門

# app.send_task('scrape_house_property_value', args=(3, 15)) # 新界/離島 － 元朗/天水圍
