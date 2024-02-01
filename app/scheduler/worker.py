from celery import Celery
from celery.schedules import crontab
import app.config
from . import hsbc,example
import concurrent.futures

settings = app.config.get_settings()

app = Celery(
    __name__,
    broker=f"{settings.redis_url}/0",
    backend=f"{settings.redis_url}/1"
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, *arg, **kwargs):
    sender.add_periodic_task(
        # crontab(minute="*"),
        30.0,
        scrape_house_property_value.s()
    )

@app.task
def scrape_house_property_value():
    # print("Start House Property Value Evaluation Scan in HSBC")
    s = example.Example()
    s.scrape()
    del s
    
    



