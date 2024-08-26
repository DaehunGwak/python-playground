import threading

import schedule

from cache.evict_schedule import clear_ttl_cache, run_clear_cache_scheduler

schedule.every(6).hours.do(clear_ttl_cache)

scheduler_thread = threading.Thread(target=run_clear_cache_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

