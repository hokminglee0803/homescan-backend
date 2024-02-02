from celery import Celery
from celery.schedules import crontab
import app.config
from app.scheduler.thread import ThreadScraper

settings = app.config.get_settings()

app = Celery(
    __name__, broker=f"{settings.redis_url}/0", backend=f"{settings.redis_url}/1"
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, *arg, **kwargs):
    sender.add_periodic_task(
        crontab(day_of_month=2),
        # 30.0,
        scrape_house_property_value.s(),
    )


@app.task
def scrape_house_property_value():
    s = ThreadScraper()
    s.scrape(1, 1) # 香港 － 香港仔
    del s
