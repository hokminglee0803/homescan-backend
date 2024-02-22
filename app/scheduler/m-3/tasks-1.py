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

app.send_task('scrape_house_property_value', args=(3,1, [13,14,15,16,17])) # 香港 － 薄扶林

# app.send_task('scrape_house_property_value', args=(1, 11)) # 香港 － 鰂魚涌

# app.send_task('scrape_house_property_value', args=(1, 12)) # 香港 － 西灣河

# app.send_task('scrape_house_property_value', args=(1, 13)) # 香港 － 筲箕灣

# app.send_task('scrape_house_property_value', args=(1, 14)) # 香港 － 大坑/渣甸山   