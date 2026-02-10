"""
    gunicorn.conf.py
"""
workers = 3
worker_class = "uvicorn.workers.UvicornWorker"

timeout = 30
max_requests = 1000
max_requests_jitter = 100

