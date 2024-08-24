from typing import List, Iterator
import re

import requests
from bs4 import BeautifulSoup, Tag

from web_scrapper.constants import REQUEST_HEADERS, PARSER_NAME
from web_scrapper.factories import get_skill_url, get_engineering_page_url
from web_scrapper.models import JobDescription


def scrap_job_descriptions() -> Iterator[List[JobDescription]]:
    page = 1
    while True:
        url = get_engineering_page_url(page)
        response = requests.get(url=url, headers=REQUEST_HEADERS)
        soup = BeautifulSoup(response.text, features=PARSER_NAME)
        jobs = _get_job_descriptions(soup)

        if len(jobs) <= 0:
            break
        page += 1

        yield jobs


def scrap_job_descriptions_by_skill(skill: str) -> List[JobDescription]:
    url = get_skill_url(skill)
    response = requests.get(url=url, headers=REQUEST_HEADERS)
    soup = BeautifulSoup(response.text, features=PARSER_NAME)
    return _get_job_descriptions(soup)


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
        description=tag.find(class_="bjs-jlid__description").text.strip(),
    )


def scrap_engineering_popular_skills() -> List[str]:
    url = get_engineering_page_url(1)
    response = requests.get(url=url, headers=REQUEST_HEADERS)
    soup = BeautifulSoup(response.text, features=PARSER_NAME)
    tags = soup.find(class_="popular_skills").find_all('a')
    return list(
        map(lambda tag: tag.get('href').split('/')[-2], tags)
    )
