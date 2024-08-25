import pprint
from typing import Iterator, List

import requests
from bs4 import BeautifulSoup, Tag

from web_scrapper.models import JobDescription, EMPTY_JOB_DESCRIPTION
from web_scrapper.web3.constants import WEB3_REQUEST_HEADERS, WEB3_PARSER_NAME
from web_scrapper.web3.factories import get_web3_tag_page_url, get_web3_job_detail_link


def scrap_web3_job_descriptions(tag: str) -> Iterator[List[JobDescription]]:
    page = 1
    before_jobs: List[JobDescription] = [EMPTY_JOB_DESCRIPTION]
    while True:
        url = get_web3_tag_page_url(tag, page)
        response = requests.get(url=url, headers=WEB3_REQUEST_HEADERS)
        soup = BeautifulSoup(response.text, features=WEB3_PARSER_NAME)
        job_descriptions: List[JobDescription] = _get_job_descriptions(soup)

        # web3 pagination 은 무한대로 가능한 '척' 하기 때문에 이전 결과인 마지막 요소와 비교하여 끝을 맺음
        if len(job_descriptions) <= 0 or before_jobs[-1] == job_descriptions[-1]:
            break
        page += 1
        before_jobs = job_descriptions

        yield job_descriptions


def _get_job_descriptions(soup: BeautifulSoup) -> List[JobDescription]:
    tbody = soup.find(class_='tbody')
    if tbody is None:
        return []

    rows = tbody.find_all('tr')
    rows = filter(lambda tag: set(tag.get_attribute_list('class')) != {'border-paid-table', 'table_row'}, rows)
    return list(map(_map_job_description_from, rows))


def _map_job_description_from(tag: Tag) -> JobDescription:
    job_title: Tag = tag.find(class_="job-title-mobile")
    job_locations: List[Tag] = tag.find_all(class_="job-location-mobile")
    regions: List[str] = list(map(lambda _tag: _tag.text, job_locations[1].find_all('a')))
    tags = tag.find_all(class_="my-badge")

    return JobDescription(
        title=job_title.find('h2').text.strip(),
        link=get_web3_job_detail_link(job_title.find('a').get('href')),
        company_name=job_locations[0].find('h3').text.strip(),
        description=f"regions: {str.join(', ', regions)} \n"
                    f"salary: {tag.find(class_='text-salary').text.strip()} \n"
                    f"badge: {str.join(', ', map(lambda _tag: _tag.find('a').text.strip(), tags))}"
    )


if __name__ == '__main__':
    results = []

    for jobs in scrap_web3_job_descriptions('python'):
        pprint.pp(jobs)
        results.extend(jobs)

    print(len(results))