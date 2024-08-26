import time

import schedule

from cache.ttl_cache import scrape_ttl_cache
from main import app


def clear_ttl_cache():
    app.logger.info("start cache clear...")
    scrape_ttl_cache.clear()
    app.logger.info("done cache clear!")


def run_clear_cache_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)
