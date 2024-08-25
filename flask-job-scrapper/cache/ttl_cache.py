from cachetools import TTLCache

scrape_ttl_cache = TTLCache(maxsize=256, ttl=60 * 60 * 6)
