web: uwsgi -s 127.0.0.1:8000 -w offline:wsgi --buffer-size=32000
worker: python -m webmonitor.start_worker
redis: redis-server ${VIRTUAL_ENV}/etc/redis.conf
