from web_scrapper.constants import REQUEST_BASE_URL
from web_scrapper.models import JobApiRequestType


def get_engineering_page_url(page: int) -> str:
    path = JobApiRequestType.ENGINEERING.value
    return f"{REQUEST_BASE_URL}{path}/page/{page}"


def get_skill_url(skill: str) -> str:
    path = JobApiRequestType.SKILL_AREAS.value
    return f"{REQUEST_BASE_URL}{path}/{skill}"
