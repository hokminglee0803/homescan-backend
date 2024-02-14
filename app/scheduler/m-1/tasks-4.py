import asyncio
from celery import Celery
from celery.schedules import crontab
import app.config
from app.scheduler.test import TestScraper
settings = app.config.get_settings()

app = Celery(
    __name__, broker=f"{settings.redis_url}/0", backend=f"{settings.redis_url}/1"
)

app.conf.beat_schedule = {
    # "hk-1": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 1)  # 香港 － 香港仔/鴨脷洲
    # },
    # "hk-2": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 2)  # 香港 － 香港仔
    # },
    # "hk-3": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 3)  # 香港 － 銅鑼灣
    # },
    "hk-4": {
        "task": "scrape_house_property_value",
        "schedule": crontab(day_of_month=14),
        'args': (1, 4)  # 香港 － 中環/上環
    },
    # "hk-5": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 5)  # 香港 － 柴灣
    # },
    # "hk-6": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 6)  # 香港 － 跑馬地/黃泥涌
    # },
    # "hk-7": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 7)  # 香港 － 南區
    # },
    # "hk-8": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 8)  # 香港 － 堅尼地城/西營盤
    # },
    # "hk-9": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 9)  # 香港 － 半山
    # },
    # "hk-10": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 10)  # 香港 － 北角
    # },
    # "hk-11": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 11)  # 香港 － 薄扶林
    # },
    # "hk-12": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 12)  # 香港 － 鰂魚涌
    # },
    # "hk-13": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 13)  # 香港 － 西灣河
    # },
    # "hk-14": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 14)  # 香港 － 筲箕灣
    # },
    # "hk-15": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 15)  # 香港 － 大坑/渣甸山
    # },
    # "hk-16": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 16)  # 香港 － 山頂
    # },
    # "hk-17": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 17)  # 香港 － 灣仔
    # },
    # "hk-18": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (1, 18)  # 香港 － 黃竹坑
    # },
    # "kl-1": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 1)  # 九龍 － 長沙灣/荔枝角
    # },
    # "kl-2": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 2)  # 九龍 － 鑽石山
    # },
    # "kl-3": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 3)  # 九龍 － 紅磡
    # },
    # "kl-4": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 4)  # 九龍 － 啟德
    # },
    # "kl-5": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 5)  # 九龍 － 九龍灣
    # },
    # "kl-6": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 6)  # 九龍 － 九龍城
    # },
    # "kl-7": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 7)  # 九龍 － 九龍塘
    # },
    # "kl-8": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 8)  # 九龍 － 觀塘/秀茂坪
    # },
    # "kl-9": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 9)  # 九龍 － 藍田
    # },
    # "kl-10": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 10)  # 九龍 － 旺角/何文田
    # },
    # "kl-11": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 11)  # 九龍 － 牛池灣/彩虹
    # },
    # "kl-12": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 12)  # 九龍 － 牛頭角
    # },
    # "kl-13": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 13)  # 九龍 － 新蒲崗/慈雲山
    # },
    # "kl-14": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 14)  # 九龍 － 深水埗
    # },
    # "kl-15": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 15)  # 九龍 － 石硤尾/又一村
    # },
    # "kl-16": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 16)  # 九龍 － 大角咀
    # },
    # "kl-17": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 17)  # 九龍 － 土瓜灣
    # },
    # "kl-18": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 10)  # 九龍 － 尖沙咀
    # },
    # "kl-19": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 19)  # 九龍 － 黃大仙/橫頭磡
    # },
    # "kl-20": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 20)  # 九龍 － 油塘/茶果嶺
    # },
    # "kl-21": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (2, 21)  # 九龍 － 油麻地
    # },
    # "nt-1": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 1)  # 新界/離島 － 粉嶺
    # },
    # "nt-2": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 2)  # 新界/離島 － 葵涌
    # },
    # "nt-3": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 3)  # 新界/離島 － 荔景
    # },
    # "nt-4": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 4)  # 新界/離島 － 大嶼山/離島
    # },
    # "nt-5": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 5)  # 新界/離島 － 馬鞍山
    # },
    # "nt-6": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 6)  # 新界/離島 － 西貢/清水灣
    # },
    # "nt-7": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 7)  # 新界/離島 － 深井/青龍頭
    # },
    # "nt-8": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 8)  # 新界/離島 － 沙田
    # },
    # "nt-9": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 9)  # 新界/離島 － 上水
    # },
    # "nt-10": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 10)  # 新界/離島 － 大埔
    # },
    # "nt-11": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 11)  # 新界/離島 － 將軍澳
    # },
    # "nt-12": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 12)  # 新界/離島 － 青衣
    # },
    # "nt-13": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 13)  # 新界/離島 － 荃灣
    # },
    # "nt-14": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 14)  # 新界/離島 － 屯門
    # },
    # "nt-15": {
    #     "task": "scrape_house_property_value",
    #     "schedule": crontab(day_of_month=14),
    #     'args': (3, 15)  # 新界/離島 － 元朗/天水圍
    # },
}


@app.task(name='scrape_house_property_value')
def scrape_house_property_value(region, district):
    s = TestScraper()
    s.scrape(selected_region=region,selected_district=district)
    del s
    # retry = 0
    # while retry < 10:
    #     try:
    #         s = ThreadScraper()
    #         s.scrape(region, district)
    #         del s
    #         retry = 10
    #     except:
    #         retry += 1
    #         time.sleep(30)
