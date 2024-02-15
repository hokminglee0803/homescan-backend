import asyncio
from datetime import timedelta
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

app.send_task('scrape_house_property_value', args=(1, 1)) # 香港 － 香港仔/鴨脷洲

app.send_task('scrape_house_property_value', args=(1, 2)) # 香港 － 香港仔

app.send_task('scrape_house_property_value', args=(1, 3)) # 香港 － 銅鑼灣

app.send_task('scrape_house_property_value', args=(1, 4)) # 香港 － 中環/上環

app.send_task('scrape_house_property_value', args=(1, 5)) # 香港 － 柴灣