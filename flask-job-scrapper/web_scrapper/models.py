from dataclasses import dataclass


@dataclass(frozen=True)
class JobDescription:
    company_name: str
    title: str
    description: str
    link: str


EMPTY_JOB_DESCRIPTION = JobDescription('', '', '', '')
