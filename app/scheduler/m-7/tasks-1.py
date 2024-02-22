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


app.send_task('scrape_house_property_value', args=(7,2, [17,18,19,20,21])) # 九龍 － 新蒲崗/慈雲山

# app.send_task('scrape_house_property_value', args=(2, 14)) # 九龍 － 深水埗

# app.send_task('scrape_house_property_value', args=(2, 15)) # 九龍 － 石硤尾/又一村

# app.send_task('scrape_house_property_value', args=(2, 16)) # 九龍 － 大角咀

# app.send_task('scrape_house_property_value', args=(2, 17)) # 九龍 － 土瓜灣
