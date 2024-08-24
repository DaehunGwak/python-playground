import re
from typing import List, Iterator

from bs4 import BeautifulSoup, Tag
from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from web_scrapper.constants import PARSER_NAME
from web_scrapper.factories import get_search_url
from web_scrapper.models import JobDescription
from web_scrapper.selenium.driver import chrome_driver


def scrap_job_descriptions(query: str) -> Iterator[List[JobDescription]]:
    page = 1
    while True:
        url = get_search_url(query=query, page=page)
        chrome_driver.get(url)
        _get_wait_search_results(chrome_driver, url)
        soup = BeautifulSoup(chrome_driver.page_source, features=PARSER_NAME)
        jobs = _get_job_descriptions(soup)

        if len(jobs) <= 0:
            break
        page += 1

        yield jobs


def _get_wait_search_results(driver: WebDriver, url: str):
    try:
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "ais-Hits"))
        )
    except TimeoutException:
        print(f"Timed out waiting for page (url: {url})")


def _get_job_descriptions(soup: BeautifulSoup) -> List[JobDescription]:
    tags: List[Tag] = soup.find_all(class_="bjs-jlid__wrapper")
    return list(
        map(_map_job_description_from, tags)
    )


def _map_job_description_from(tag: Tag) -> JobDescription:
    title_header: Tag = tag.find(class_="bjs-jlid__h").findChild()
    return JobDescription(
        title=title_header.text,
        link=title_header.get('href'),
        company_name=tag.find(class_="bjs-jlid__b").text,
        description=re.sub(r'\n', " | ", tag.find(class_="bjs-jlid__description").text.strip()),
    )
