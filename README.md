# homescan-backend

Start Fast API
python3 -m uvicorn app.main:app --reload --log-config=app/log_conf.yaml

Start Worker
python3 -m celery -A app.scheduler.tasks:app worker -l info -c 53

Start Beat
python3 -m celery -A app.scheduler.tasks:app beat -l info
