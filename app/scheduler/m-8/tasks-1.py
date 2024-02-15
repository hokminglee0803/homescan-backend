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

app.send_task('scrape_house_property_value', args=(2, 18)) # 九龍 － 尖沙咀

app.send_task('scrape_house_property_value', args=(2, 19)) # 九龍 － 黃大仙/橫頭磡

app.send_task('scrape_house_property_value', args=(2, 20)) # 九龍 － 油塘/茶果嶺

app.send_task('scrape_house_property_value', args=(2, 21)) # 九龍 － 油麻地

app.send_task('scrape_house_property_value', args=(3, 1)) # 新界/離島 － 粉嶺
