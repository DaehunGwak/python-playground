from web_scrapper.berlinstartup.constants import REQUEST_BASE_URL


def get_search_url(query: str, page: int) -> str:
    return f"{REQUEST_BASE_URL}/?s={query}&page={page}"
