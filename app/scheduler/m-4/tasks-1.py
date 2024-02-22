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

# app.send_task('scrape_house_property_value', args=(1, 15)) # 香港 － 山頂

# app.send_task('scrape_house_property_value', args=(1, 16)) # 香港 － 灣仔

# app.send_task('scrape_house_property_value', args=(1, 17)) # 香港 － 黃竹坑

app.send_task('scrape_house_property_value', args=(4,2, [1,2,3,4,5,6])) # 九龍 － 長沙灣/荔枝角

# app.send_task('scrape_house_property_value', args=(2, 2)) # 九龍 － 鑽石山