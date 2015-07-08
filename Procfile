#web: gunicorn offline:wsgi
web: python run.py
worker: python -m webmonitor.start_worker
#redis: redis-server ${VIRTUAL_ENV}/etc/redis.conf
