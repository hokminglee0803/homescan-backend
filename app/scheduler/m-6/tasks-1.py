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
    s.scrape(thread_idx=thread,selected_region=region,selected_district=district)
    del s

app.send_task('scrape_house_property_value', args=(6,2, [12,13,14,15,16])) # 九龍 － 觀塘/秀茂坪

# app.send_task('scrape_house_property_value', args=(2, 9)) # 九龍 － 藍田

# app.send_task('scrape_house_property_value', args=(2, 10)) # 九龍 － 旺角/何文田

# app.send_task('scrape_house_property_value', args=(2, 11)) # 九龍 － 牛池灣/彩虹

# app.send_task('scrape_house_property_value', args=(2, 12)) # 九龍 － 牛頭角