from config.celery import app
import logging


logger = logging.getLogger(__name__)

@app.task(time_limit=2500)
def archive_processor():
    print('hello')

