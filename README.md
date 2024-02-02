# homescan-backend

Start Fast API
python3 -m uvicorn app.main:app --reload --log-config=app/log_conf.yaml

Start Worker
python3 -m celery -A app.scheduler.hk.hk-1:app worker -P solo -l info
python3 -m celery -A app.scheduler.hk-2:app worker -P solo -l info

Start Beat
python3 -m celery -A app.scheduler.hk-1:app beat -l debug
python3 -m celery -A app.scheduler.hk-2:app beat -l debug
