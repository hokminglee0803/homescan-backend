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

app.send_task('scrape_house_property_value', args=(2,1, [7,8,9,10,11,12])) # 香港 － 跑馬地/黃泥涌

# app.send_task('scrape_house_property_value', args=(1, 6)) # 香港 － 南區

# app.send_task('scrape_house_property_value', args=(1, 7)) # 香港 － 堅尼地城/西營盤

# app.send_task('scrape_house_property_value', args=(1, 8)) # 香港 － 半山

# app.send_task('scrape_house_property_value', args=(1, 9)) # 香港 － 北角   