# homescan-backend

Start Fast API
python3 -m uvicorn app.main:app --reload --log-config=app/log_conf.yaml

Start Worker
python3 -m celery -A app.scheduler.worker:app worker -P solo -l info

Start Beat
python3 -m celery -A app.scheduler.worker:app beat -l debug
