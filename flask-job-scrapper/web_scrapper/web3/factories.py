from web_scrapper.web3.constants import WEB3_BASE_URL


def get_web3_tag_page_url(tag: str, page: int) -> str:
    return f"{WEB3_BASE_URL}/{tag}-jobs?page={page}"


def get_web3_job_detail_link(path: str) -> str:
    return f"{WEB3_BASE_URL}{path}"
