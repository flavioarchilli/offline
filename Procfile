web: gunicorn monitoring_app:wsgi
worker: python -m jobmonitor.start_worker
redis: redis-server /usr/local/etc/redis.conf
